import pandas as pd
import numpy as np
import string, json
from pdia.responseReconstruction.num2alpha import num2alpha

def parseKeyValuePairs_BQChoice(row, config):
    """
    Given response process data row with a key-value pair like {u'VHXXXXXX_4': u'checked'}, parse the
    key-value pair and return {"Option":s, "Action":action}
    :param row: a row in process data
    :param config: the config obj passed down
    :return: {"Option":s, "Action":action} or None
    """
    assert (isinstance(row, pd.Series))

    # make sure extInfo is a dict
    try:
        if (isinstance(row[config["extInfoColumn"]], str)):
            extInfostring = row[config["extInfoColumn"]].replace("'", '\"').replace('u"', '"')
            thisExtInfo = json.loads(extInfostring)
        else:
            thisExtInfo = row[config["extInfoColumn"]]
    except:
        return None

    if thisExtInfo is None:
        return None

    s = ""; action = ""; accnum=""
    for key, value in thisExtInfo.items():
        # example: {u'VHXXXXXX_4': u'checked'}
        try:
            accnum, option = key.replace('"', '').split("-")
            s = num2alpha(option)
            action = value.replace('"', "")
            # make sure the response is for the current accnum
            # this does not apply to BQChoice, which has a common AccNum in addition to
            # assert (accnum == row["AccessionNumber"])
        except Exception as e:
            # logger.error("reconMC:")
            # logger.exception(e)
            # exc_buffer = StringIO.StringIO()
            # traceback.print_exc(file=exc_buffer)
            # logger.error('Uncaught exception in worker process:\n%s', exc_buffer.getvalue())
            # skip the current key/value pair
            continue
    return None if action == "" else {"ChildAccNum":accnum, "Option": s, "Action": action}



def expandBQChoicesRow(row):
    """Loop through elements in ReconstructedAnswer and return a df that is one-row each for each element"""
    reconAnswer = row["ReconstructedAnswer"]
    res = []
    for item in reconAnswer:
        res.append({
            "BookletNumber": row["BookletNumber"],
            "BlockCode": row["BlockCode"],
            "AccessionNumber": row["AccessionNumber"],
            "ResponseComponentId": "item-" + row["AccessionNumber"] + "-" + item["accnum"],
            "ReconstructedAnswer": [item["response"]]
        })
    return res


def postProcessObsBQChoicesResp(dfObsBQChoicesResp):
    if dfObsBQChoicesResp.shape[0] > 0:
        # expand the list in each AccNum into several rows
        # return pd.DataFrame(dfObsBQChoicesResp.apply(expandBQChoicesRow, axis=1).sum())

        # BUG: there is a mysterious bug in the above that just wouldn't return the right df for some data
        # It loosk like it's not applying the function to the expandBQChoicesRow when using apply(, axis=1),
        # at least when the df contains only 1 item's data. The same function applied using .iloc[0] works,
        # and the iterrows() works as well.
        tmp=[]
        for idx, row in dfObsBQChoicesResp.iterrows():
            tmp.append(pd.DataFrame(expandBQChoicesRow(row)))
        return pd.concat(tmp)
    else:
        return None


def reconBQChoice(itemLog, config):
    """
    Given the process data log of a BQChoice item, reconstruct the item response (and a lot of other information).
    Each BQChoice is essentially a collection of MCSS items, with all their features.

    We take care of the ClearAnswer problem in BQChoice, but not any of the elimination strategies as we don't
    have evidence that this is a problem. The final reconstructed responses, however, is based on the "strict
    rule", meaning that if one uses the "ClearAnswer" button at the end, we interpret it as intended and will
    return a blank answer.

    config is something like
    configBQChoices = {
        "byVars": ["BookletNumber", "BlockCode"],
        "itemtypeColumn": "ItemTypeCode",
        "accnumColumn": "AccessionNumber",
        "outputColumn": "ReconstructedAnswer",
        "dispatcher": reconItemResponses,
        "postprocessor": postProcessObsBQChoicesResp,
        "handlers": {
            "BQChoices": reconBQChoice
        }
    }

    *bug*: Note that the 2017 BQChoice log had a bug where if a student changes mind from option 1 to 2, it logs
    the following erroneous event sequences (pdia bug#129):
    - option1 selected
    - option2 selected + option2 unselected (in random order), instead of option1 unselected + option2 selected

    Solution:
    - check for events with exact timestampes
    - check if they are the same sub-item, one check and the other uncheck
    - subtract 1ms from the uncheck event, resort the data frame, so that it's not the last event.

    :param itemLog: a data fram containing the log of a single MC item
    :param config: a configuration dict
    :return: a Pandas series of the reconstructed responses.

    """
    assert (isinstance(itemLog, pd.DataFrame))
    assert (isinstance(config, dict))
    assert ("maxNumberOfOptions" in config)
    assert (config["itemtypeColumn"] in itemLog.columns)
    assert (config["accnumColumn"] in itemLog.columns)
    assert (config["extInfoColumn"] in itemLog.columns)
    # only a single item
    assert (len(itemLog[config["accnumColumn"]].unique()) == 1)
    # only a single item type
    assert (len(itemLog[config["itemtypeColumn"]].unique() ) == 1)


    # drop trailing Clear Answers
    # here we do a trick:
    # We reverse the row orders, and loop through rows from the top
    # We keep the index of rows that are "Clear Answer" events, until
    # we hit the first event that is not. Then we exit the loop
    clearAnswer = False
    reversed_df = itemLog.iloc[::-1].reset_index()
    droppedrows = []
    # response history: need to do so before removing the trailing Clear Answers
    responseHistory = []
    for index, row in reversed_df.iterrows():
        if (row.Label == "Clear Answer"):
            droppedrows.append(index)
            clearAnswer = True
            responseHistory.append("X")
        else:
            # first non-clearAnswer event from the back; stop
            break
    # if there are trailing clearAnswer, then we drop the corresponding rows by index
    # and we reverse the row order again, to get a df without the trailing ClearAnswer events
    if (clearAnswer):
        reversed_df.drop(reversed_df.index[droppedrows], inplace=True)
    itemLog = reversed_df.iloc[::-1]

    # init
    selection = {}
    elimination = {}
    hist = []

    # Dealing with the bug with uncheck events; pdia bug #129
    itemLog.EventTime = pd.to_datetime(itemLog.EventTime)
    # find the 2nd rows with duplicated timestamps; this is getting the last occurances
    idx = itemLog.EventTime == itemLog.EventTime.shift()
    # check if these are uncheck events; handle None cases
    idx = idx & itemLog.loc[idx, "extInfo"].apply(lambda r: r[list(r.keys())[0]] == "unchecked" if r is not None else False)
    # we change the timestamp such that the uncheck event will come before the checked event
    # in the case the user intended to uncheck an answer, presumably this won't happen 0ms after the selection
    itemLog.loc[idx, "EventTime"] = itemLog.loc[idx, "EventTime"] - np.timedelta64(1, 'ms')
    itemLog.sort_values(by=["EventTime"], inplace=True)

    # looping through all actions from the top, just to get a list of all accnum-option combos
    # now the key to each dict is accnum-option, as in "VH8888-A".
    for index, row in itemLog.iterrows():
        kv = parseKeyValuePairs_BQChoice(row, config=config)
        if kv is None:
            continue
        i = "{}-{}".format(kv["ChildAccNum"], kv["Option"])
        selection[i] = False
        elimination[i] = False

    # looping through all actions again, to process
    for index, row in itemLog.iterrows():
        if (row['Label'] == 'Clear Answer'):
            # these are real clear answer events that we should honor, for MCSS or MCMS
            for k in selection:
                selection[k] = False
            # elimination status is cleared??
            # for k in elimination:
            #     elimination[k] = False
            # append history
            hist.append('X')
        else:
            kv = parseKeyValuePairs_BQChoice(row, config=config)
            if kv is None:
                continue
            accnum = kv["ChildAccNum"]
            option = kv["Option"]
            action = kv["Action"]
            key = "{}-{}".format(accnum, option)

            if (row['Label'] == 'Eliminate Choice'):
                if (action == 'eliminated'):
                    elimination[key] = True
                    # unlike Reading, where -A also genrates another event to clear selection_A
                    # math does not have an explicit event. We need to recreate this
                    # If option X is eleiminated, X is also de-selected
                    selection[key] = False
                    hist.append('-{}'.format(key))
                elif (action == 'uneliminated'):
                    elimination[key] = False
                    # Uneliminate does not reinstate the selection state. If option X uneliminated
                    # its selection state is always False regardless of history
                    # no need to change anything here.
                    hist.append('+{}'.format(key))
                else:
                    pass
            elif row['Label'] == 'Click Choice':
                if (action == 'checked'):
                    # selecting option X means 2 things :
                    # a), for BQChoice all other options of the same child-accnum are cleared
                    for i in selection:
                        if i.startswith(accnum):
                            selection[i] = False
                    # b), X cannot be in the eliminated state
                    elimination[key] = False
                    # now we set the selection to True
                    selection[key] = True
                    hist.append('@{}'.format(key))
                elif action == 'unchecked':
                    # for BQChoice this simply sets the key to False.
                    selection[key] = False
                    hist.append('^{}'.format(key))
                else:
                    pass
            else:
                # not supposed to happen
                pass

    # responseHistory contruction: take hist and the trailing clearAnswer events
    responseHistory = " ".join(hist + responseHistory)

    # now return
    res = {
        "ResponseHistory": responseHistory,
        "XRule": [],
        "StrictRule": [],
        "ReconstructedAnswer": []
    }
    # for BQChoice reconItemResponses, we want something like [{accnum: "VHXXXXXX", "response":"A"}, ...]
    # first filter out all selections that are False, i.e., choosen once but then discarded
    xRule = [key for key, val in list(selection.items()) if val is True]
    for key in xRule:
        accnum, option = str(key).split("-")
        res["XRule"].append({"accnum":accnum, "response":option})
    # now parse the keys in the chosen options; the keys are like accnum-option
    res["StrictRule"] = [] if clearAnswer == True else res["XRule"]
    # answer = strict rule, unless otherwise specified, sans some reserved keywords
    res["ReconstructedAnswer"] = [i for i in res["StrictRule"] if i not in ['response', 'response']]

    return pd.Series(res)
