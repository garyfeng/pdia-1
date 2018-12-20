import pandas as pd
import json
import string
from pdia.responseReconstruction.num2alpha import num2alpha


def parseKeyValuePairs_MC(row, config):
    """
    Given response process data row with a key-value pair like {u'VHXXXXXX_4': u'checked'}, parse the
    key-value pair and return {"Option":s, "Action":action}

    config is something like
    configENAEP = {
        "byVars": ["BookletNumber", "BlockCode"],
        "itemtypeColumn": "ItemTypeCode",
        "accnumColumn": "AccessionNumber",
        "outputColumn": "ReconstructedAnswer",
        "extInfoColumn": "extInfo",
        "maxNumberOfOptions": 10,
        "dispatcher": reconItemResponses,
        "postprocessor": postProcessObsENAEPResp,
        "handlers": {
            "BQMCSS": reconMCSS,
            "BQMCMS": reconMCMS,
            "MCSS": reconMCSS,
            "MCMS": reconMCMS
        }
    }

    :param row: a row in process data
    :param config: a configuration dict for the processing.
    :return: {"Option":s, "Action":action} or None
    """
    assert (isinstance(row, pd.Series))
    assert (isinstance(config, dict))
    assert (config["itemtypeColumn"] in row)
    assert (config["accnumColumn"] in row)
    assert (config["extInfoColumn"] in row)

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

    s = ""
    action = ""
    accnum, option = ["InvalidAccNum", "InvalidOption"]

    for key, value in thisExtInfo.items():
        # example: {u'VHXXXXXX_4': u'checked'}
        try:
            accnum, option = key.replace('"', '').split("_")
            s = num2alpha(option, maxNumberOfOptions=8)
            action = value.replace('"', "")
            # #### actually, this is not always the case. see issue #138 ########
            # make sure the response is for the current accnum
            # assert (accnum == row[config["accnumColumn"]])
        except Exception as e:
            # logger.error("reconMC:")
            # logger.exception(e)
            # exc_buffer = StringIO.StringIO()
            # traceback.print_exc(file=exc_buffer)
            # logger.error('Uncaught exception in worker process:\n%s', exc_buffer.getvalue())
            # skip the current key/value pair
            continue
    return None if action == "" else {"Option": s, "Action": action, "ResponseAccNum": accnum}


def reconMC(itemLog, config, singleChoice=True):
    """
    Given the process data log of a MCSS item, reconstruct the item response (and a lot of other information).

    We need to reconstruct two sets of states for each option:
    - Selection: which option is being selected
    - Elimination: which options is being eliminated

    In addition, the algorithm also tries to deal with several known student response patterns, including:
    - Using the "Clear Answer" button as if it's the "Submit Answer" button. We ignore the trailing Clear Answer
        buttons, while still honoring the intermediate Clear Answer buttons
    - Using the "Eliminating option" buttons as a response mechanism. There are two variations of this.
        a). Eliminating a single option without making a choice, as if marking it elimated is the positive response
        b). Eliminating all options but one, as a way to indicate selection of the remaining option

    The algorithm tracks the state of the selection, elimination, and clear answers. Returned data is a Pandas Series:
        "responseHistory": the responseHistory,
        "Selection_A"-"Selection_E": whether each option is selected, True or False
        "Eliminate_A"-"Eliminate_E": whether each option is eliminated, True or False
        "E1_Rule": the would-be response by the "Elimination-1 rule", i.e., if the answer is chosen by eliminating only 1 option
        "E3_Rule": the would-be response by the "Elimination-3 rule", i.e., if the answer is chosen by eliminating all but 1 option
        "X_Rule": the would-be response by ignoring trailing Clear Answer events
        "Strict_Rule": the official response
        "Answer" : -- currently set to the Strict_Rule; in a list format.

    config is something like
    configENAEP = {
        "byVars": ["BookletNumber", "BlockCode"],
        "itemtypeColumn": "ItemTypeCode",
        "accnumColumn": "AccessionNumber",
        "outputColumn": "ReconstructedAnswer",
        "extInfoColumn": "extInfo",
        "maxNumberOfOptions": 10,
        "dispatcher": reconItemResponses,
        "postprocessor": postProcessObsENAEPResp,
        "handlers": {
            "BQMCSS": reconMCSS,
            "BQMCMS": reconMCMS,
            "MCSS": reconMCSS,
            "MCMS": reconMCMS
        }
    }

    :param itemLog: a data fram containing the log of a single MC item
    :param singleChoice: whether only 1 option is allowed to be selected; default to True
    :param config: a dict with configuration info
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
    assert (len(itemLog[config["itemtypeColumn"]].unique()) == 1)
    # assert (itemLog["ItemTypeCode"].unique() == "MCSS")

    maxNumberOfOptions = config["maxNumberOfOptions"]

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
        if (row["Label"] == "Clear Answer"):
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
    # set responseAccNum to default to item accnum
    responseAccNum = itemLog[config["accnumColumn"]].iloc[0]

    # get optin list, using num2alpha() to also handle out of range values
    # optionList = string.ascii_uppercase[:maxNumberOfOptions]
    optionList = [num2alpha(i, maxNumberOfOptions=8) for i in range(1, maxNumberOfOptions)]

    for i in optionList:
        selection[i] = False
        elimination[i] = False

    # track states by looping through all actions from the top, less the trailing CAs
    for index, row in itemLog.iterrows():
        # set default responseAccNum to the item's 'AccessionNumber'
        responseAccNum = row[config["accnumColumn"]]
        if (row['Label'] == 'Clear Answer'):
            # these are real clear answer events that we should honor, for MCSS or MCMS
            for a in selection:
                selection[a] = False
            hist.append('X')
        else:
            kv = parseKeyValuePairs_MC(row, config=config)
            if kv is None:
                continue
            option = kv["Option"]
            action = kv["Action"]
            responseAccNum = kv["ResponseAccNum"]

            if row['Label'] == 'Eliminate Choice':
                if action == 'eliminated':
                    elimination[option] = True
                    # unlike Reading, where -A also genrates another event to clear selection_A
                    # math does not have an explicit event. We need to recreate this
                    # If option X is eleiminated, X is also de-selected
                    selection[option] = False
                    hist.append('-{}'.format(option))
                elif action == 'uneliminated':
                    elimination[option] = False
                    # Uneliminate does not reinstate the selection state. If option X uneliminated
                    # its selection state is always False regardless of history
                    # no need to change anything here.
                    hist.append('+{}'.format(option))
                else:
                    pass
            elif row['Label'] == 'Click Choice':
                if action == 'checked':
                    # selecting option X means 2 things :
                    # a), for MCSS all other options are cleared
                    if singleChoice:
                        for i in selection:
                            selection[i] = False
                    # b), X cannot be in the eliminated state
                    elimination[option] = False
                    # now we set the selection to True
                    selection[option] = True
                    hist.append('@{}'.format(option))
                elif action == 'unchecked':
                    # for MCSS this should not matter, because a change of mind auto clears the other options
                    # this can happen for MCMS cases.
                    if not singleChoice:
                        selection[option] = False
                        hist.append('^{}'.format(option))
                else:
                    pass
            else:
                # not supposed to happen
                pass

    # if no history, then we return None
    if len(hist) == 0:
        return None

    # responseHistory contruction: take hist and the trailing clearAnswer events
    responseHistory = " ".join(hist + responseHistory)

    # now return
    # we set ResponseComponentId to the itemAccNum
    res = {
        # "ResponseComponentId": "item-{}".format(responseAccNum),
        # "ItemAccNum": "item-{}".format(row["AccessionNumber"]),
        "ResponseComponentId": "item-{}".format(row["AccessionNumber"]),
        "ItemAccNum": "item-{}".format(responseAccNum),
        "ResponseHistory": responseHistory,
        "Eliminated": [],
        "E1Rule": [],
        "E3Rule": [],
        "XRule": [],
        "StrictRule": [],
        "ReconstructedAnswer": []
    }

    # response: if only one is chosen, regardless of trailing ClearAnswer buttons
    sel = [selection[k] for k in optionList]
    eli = [elimination[k] for k in optionList]
    # for MCSS, we enforce the choice==1 rule
    if singleChoice:
        if sel.count(True) == 1:
            try:
                res["XRule"] = list(optionList[sel.index(True)])
            except:
                pass
        # According to the strict rule where we treat Clear Answer literally
        res["StrictRule"] = [] if clearAnswer == True else res["XRule"]

        # Eliminate 1 Rule: use -D to indicate D as the option
        if eli.count(True) == 1:
            try:
                res["E1Rule"] = list(optionList[eli.index(True)])
            except:
                pass
        # Eliminate 3 Rule: using -A, -B, -C to indicate D is the option
        # In math where there can be up to 5 choices, "E3" is a misnomer
        # We really meant eliminating all-but-one
        if eli.count(False) == 1:
            try:
                res["E3Rule"] = list(optionList[eli.index(False)])
            except:
                pass
    else:
        # MCMS: no E* rules; also no order of selection is kept
        res["XRule"] = [optionList[i] for i, val in enumerate(sel) if val is True]
        res["StrictRule"] = [] if clearAnswer == True else res["XRule"]

    # elimination
    res["Eliminated"] = [optionList[i] for i, val in enumerate(eli) if val is True]
    # answer = strict rule, unless otherwise specified, excluding 'response'
    res["ReconstructedAnswer"] = [i for i in res["StrictRule"] if i not in ['response', 'response']]

    return pd.Series(res)


def reconMCSS(itemLog, config):
    """
    Reconstruction function for MCSS. It simply calls reconMC with singleChoice=True

    config is something like
    configENAEP = {
        "byVars": ["BookletNumber", "BlockCode"],
        "itemtypeColumn": "ItemTypeCode",
        "accnumColumn": "AccessionNumber",
        "outputColumn": "ReconstructedAnswer",
        "extInfoColumn": "extInfo",
        "maxNumberOfOptions": 10,
        "dispatcher": reconItemResponses,
        "postprocessor": postProcessObsENAEPResp,
        "handlers": {
            "BQMCSS": reconMCSS,
            "BQMCMS": reconMCMS,
            "MCSS": reconMCSS,
            "MCMS": reconMCMS
        }
    }

    :param itemLog: a data fram containing the log of a single MC item
    :param config: the config object
    :return: a Pandas series of the reconstructed responses.
    """
    return reconMC(itemLog, singleChoice=True, config=config)


def reconMCMS(itemLog, config):
    """
    Reconstruction function for MCMS. It simply calls reconMC with singleChoice=False

    config is something like
    configENAEP = {
        "byVars": ["BookletNumber", "BlockCode"],
        "itemtypeColumn": "ItemTypeCode",
        "accnumColumn": "AccessionNumber",
        "outputColumn": "ReconstructedAnswer",
        "extInfoColumn": "extInfo",
        "maxNumberOfOptions": 10,
        "dispatcher": reconItemResponses,
        "postprocessor": postProcessObsENAEPResp,
        "handlers": {
            "BQMCSS": reconMCSS,
            "BQMCMS": reconMCMS,
            "MCSS": reconMCSS,
            "MCMS": reconMCMS
        }
    }

    :param itemLog: a data fram containing the log of a single MC item
    :param config: the config object
    :return: a Pandas series of the reconstructed responses.
    """
    return reconMC(itemLog, singleChoice=False, config=config)


def fixBilingualAccNum(df):
    """
    In the case students switched language in the middle of an item, the accnum of the item changes. It's possible
    that the same item produces more then 1 reconstructed responses under different accnums. This function is meant
    to be used with groupby().

    In this case, typically only one of them has a complete response, and the other(s) is NaN. We will keep only
    the row with complete answer, dropping others.

    :param df: a data frame of reconstructed responses for a student/block/ResponseComponentId, potentially multi-row
    :return: a df with a single row with the complete reconstructed response; raising error if multiple responses
    """

    if df.shape[0] > 1:
        # df = df.loc[(df.ReconstructedAnswer.notnull() & df.ResponseHistory.notnull())]
        df = df.loc[df.ReconstructedAnswer.notnull()]
        if df.shape[0] == 1:
            return df
        else:
            # todo: failing for now. will need to actually fix this.
            raise ValueError('fixBilingualAccNum: there are no or more than one rows having complete answers')
    else:
        return df
