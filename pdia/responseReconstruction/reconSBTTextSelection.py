import pandas as pd
from pdia import logger

def truncate(s):
    substring_list=['MCSS','TXT','TXTS']
    if any(substring in str(s) for substring in substring_list):
        return str(s).rsplit('.',1)[0]
    else:
        return s

def postProcessSBTTextSelectionResp(dfSBTTextSelectionResp):
    """
    Auxilary function to post-process TextSelection responses for SBTs. The input df is is output from
    reconSBTTextSelection().

    It's a Series with reset_index() applied; therefore the var of interst is dfSBTTextSelectionResp[0], which contains
    [{'ExtractedAnswer': 'selection-22', 'ResponseComponentId': 'item-SelectExamples'}]

    We then take the df with many of these, return something like ['selection-22', 'selection-23', 'selection-27'] for
    each BookletNumber, BlockId, and ResponseComponentId.

    We will use a 2-level groupby(). The first level is to make sure we keep the ["BookletNumber", "BlockCode"] info.
    The second level, we create a new df based on ResponseComponentId and ExtractedAnswer, then combine ExtractedAnswer
    for each ResponseComponentId, creating a sorted list as output. We do a little clearn up to ensure the output df
    has the column names we wanted.

    :param dfSBTTextSelectionResp: the output from reconSBTTextSelection()
    :return: a df with columns ["BookletNumber","BlockCode","ResponseComponentId","ExtractedAnswer"]; None if response is empty
            or error.
    """
    
#    print "From postProcessSBTTextSelectionResp"

    if dfSBTTextSelectionResp is None:
        logger.error("postProcessSBTTextSelectionResp: dfSBTTextSelectionResp is None")
        return None

    if "ResponseComponentId" not in dfSBTTextSelectionResp.columns:
        try:
            #logger.error("postProcessSBTTextSelectionResp: ResponseComponentId not in dfSBTTextSelectionResp.columns")
            #logger.error("\n{}".format(dfSBTTextSelectionResp))
            dfSBTTextSelectionResp["ResponseComponentId"] = dfSBTTextSelectionResp["ControlId"].apply(truncate)
        except:
            return None

 #   print dfSBTTextSelectionResp["ResponseComponentId"]

    if dfSBTTextSelectionResp.shape[0] > 0:
        # condense this by ResponseComponentId
        try:
            # first, melt the data to multiple rows per ResponseComponentId
            res = dfSBTTextSelectionResp.groupby(["BookletNumber", "BlockCode"]) \
                .apply(lambda df: pd.DataFrame(df["ReconstructedAnswer"].sum())) \
                .reset_index()
            # now recast to one row per ResponseComponentId, with responses in a list and sorted
            res= res.groupby(["BookletNumber", "BlockCode", "ResponseComponentId"]) \
                .apply(lambda df: df["ReconstructedAnswer"].sort_values().tolist()) \
                .rename("ReconstructedAnswer").reset_index()
            return res
        except Exception as e:
            logger.error("postProcessSBTTextSelectionResp:")
            logger.exception(e)
            logger.debug(dfSBTTextSelectionResp)
            return None

    else:
        return None


def reconSBTTextSelection(itemLog, accnum="ControlId", itemtype="Label"):
    """
    Given a Pandas data frame containing the log for one item, return the reconstructed response.

    Examples of how select.toggle works:

    Label == "select.toggle"
    extendedInfo == {u'to': u'true', u'from': u'false'}
    controlId == "item-SelectExamples-selection-22"
    ...

    ==> {"ResponseComponentId": "item-SelectExamples", "ExtractedAnswer" = [selection-22, selection-23, selection-27]}

    The trick is that when we process by controlId, we can't put the the selections for each item back as a list.
    We will do this using a post-processing function, which will scan all item of this type, and combine ones with
    the same ResponseComponentId as a list.

    So for now, we will process one action at a time. We will have to run through each line and track the selection
    and deselection of each unit of selection.

    :param itemLog: a data fram containing the log of a single TextSelection select.toggle item
    :param accnum: the column name that identifies items
    :param itemtype: the column name that identifies the item type
    :return: a Pandas series of the reconstructed responses.

    """
    assert (isinstance(itemLog, pd.DataFrame))
    assert("extInfo" in itemLog.columns)
    # only a single item
    assert (itemLog[accnum].nunique() == 1)
    # only a single item type
    assert (itemLog["ItemTypeCode"].nunique() == 1)

    # return the last content
    try:
        res=[]
        lastRow = itemLog\
            .loc[itemLog[itemtype] == "select.toggle"]\
            .iloc[-1]
        response = lastRow.extInfo["to"]
        controlId = lastRow[accnum]
        # if this is not an "unselect" event
        if response == "true":
            # for "item-SelectExamples-selection-22"
            # for "slide10questions-option-2"
            for delimitor in ["_Selection", "_String"]:
                if delimitor in controlId:
                    tmplist = controlId.split(delimitor)
                    if len(tmplist) == 2:
                        # we should get 2 parts
                        res.append({"ResponseComponentId": "{}".format(tmplist[0]),
                                    "ReconstructedAnswer": "{}".format(tmplist[1])})
                    else:
                        # error parsing this response: return controlId
                        res.append({"ResponseComponentId": "{}".format(controlId),
                                    "ReconstructedAnswer": "{}".format(controlId)})
                    break # quite the loop if processed
            # if no match, this is a case of "controlId == True"; i.e.,
            # we return
            if len(res) == 0:
                res = [{"ResponseComponentId": "{}".format(controlId),
                        "ReconstructedAnswer": "{}_Selected".format(controlId)}]
    except Exception as e:
        logger.error("reconSBTTextSelection:")
        logger.exception(e)
        # logger.debug(itemLog)
        res = [{"ResponseComponentId": "ERROR_reconSBTTextSelection",
                "ReconstructedAnswer": "ERROR_reconSBTTextSelection"}]
    return res


# configSBTTextSelectionResponses = {
#     "byVars": ["BookletNumber", "BlockCode"],
#     "itemtypeColumn": "Label",
#     "accnumColumn": "ControlId",
#     "outputColumn": "ReconstructedAnswer",
#     "extInfoColumn": "extInfo",
#     "dispatcher": reconSBTItemResponses,
#     "postprocessor": postProcessSBTTextSelectionResp,
#     "handlers": {
#         "select.toggle": reconSBTTextSelection
#     }
# }
