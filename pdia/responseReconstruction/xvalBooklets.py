import pandas as pd
from IPython.core.display import display, HTML
from pdia import logger
from pdia.responseReconstruction.extractMC import extractMCResponse
from pdia.responseReconstruction.extractTextSelectionResponse import extractTextSelectionResponse
from pdia.responseReconstruction.extractMatchingtResponse import extractMatchingtResponse
from pdia.responseReconstruction.extractTextResponse import extractTextResponse
from pdia.responseReconstruction.extractSelectionResponses import extractSelectionResponse

from pdia.responseReconstruction.reconItemResponses import reconItemResponses
from pdia.responseReconstruction.reconMC import reconMCSS, reconMCMS, fixBilingualAccNum
from pdia.responseReconstruction.reconBQChoice import reconBQChoice, postProcessObsBQChoicesResp
from pdia.responseReconstruction.parseItemResponses import parseItemResponses

from pdia.responseReconstruction.reconSBTItemResponses import reconSBTItemResponses
from pdia.responseReconstruction.reconSBTSelectChoice import reconSBTSelectChoice
from pdia.responseReconstruction.reconSBTSelectDrop import reconSBTSelectDrop
from pdia.responseReconstruction.reconSBTText import reconSBTText
from pdia.responseReconstruction.reconSBTTextSelection import postProcessSBTTextSelectionResp,\
    reconSBTTextSelection


def reconByConfig(df, config):
    """
    Auxilury function to reconstruct responses using a particular configuration.

    It takes an observable data frame df that is already pre-filtered to contain a certain events,
    groupby the typical variables (BookletNumber and BlockCode), run the reconstruction function (aka "dispatcher")
    before running teh "postprocessor" function to clean up the output.

    :param df: the observable data frame, typically containing a single event type
    :param config: the configuration dict with required field.
    :return: the reconstructed data frame, or an empty data frame if errors occur
    """

    assert("byVars" in config)
    assert("dispatcher" in config)
    assert("postprocessor" in config)
    # config the parser function
    try:
        res = df.groupby(config["byVars"])\
            .apply(config["dispatcher"], config=config).reset_index()\
            .pipe(config["postprocessor"])
    except Exception as e:
        logger.error("reconByConfig:")
        #logger.error("input df:\n{}".format(df))
        logger.exception(e)
        res = pd.DataFrame()
    return res


def postProcessObsENAEPResp(dfObsENAEPResp):
    """
    Post processing for typically reconstructed eNAEP item types, where we add the ResponseComponentId column and
    drop useless ones.

    :param dfObsENAEPResp: the data frame containing reconstructed responses from eNAEP itemtypes
    :return: a data frame of responses with ResponseComponentId column filled in, or None
    """
    if dfObsENAEPResp.shape[0] > 0:
        # if ResponseComponentId is not set, it's set to default here
        idx = dfObsENAEPResp["ResponseComponentId"].isnull()
        dfObsENAEPResp.loc[idx, "ResponseComponentId"] = "item-" + dfObsENAEPResp.loc[idx, "AccessionNumber"]

        # can't specify for MCSS only but trying to fix the bilingual accNum bug
        # dfObsENAEPResp = dfObsENAEPResp\
        #     .groupby(["BookletNumber", "BlockCode", "ResponseComponentId"]) \
        #     .apply(fixBilingualAccNum)

        return dfObsENAEPResp.loc[:, ['BookletNumber', 'BlockCode', "AccessionNumber", "ResponseComponentId",
                                      'ReconstructedAnswer', 'ResponseHistory']]
    else:
        return None

def truncate(s):
    substring_list=['MCSS','MCMS','TXT','TXTS']
    if any(substring in str(s) for substring in substring_list):
        return str(s).rsplit('.',1)[0]
    else:
        return s

def postProcessObsSBTResp(dfObsSBTResp):
    """
    Post processing for SBT reconstruction, where we made sure the column ResponseComponentId is set.

    :param dfObsSBTResp: the data frame containing reconstructed responses from SBTs
    :return: a data frame of reconstructed responses from SBTs with the ResponseComponentId column, or None
    """
    if dfObsSBTResp.shape[0]>0:
        dfObsSBTResp.columns = ['BookletNumber', 'BlockCode', 'level_2', 'ControlId', 'ReconstructedAnswer']
        dfObsSBTResp["ResponseComponentId"] = dfObsSBTResp["ControlId"].apply(truncate)
#        dfObsSBTResp.drop(['ControlId'],axis=1)
        return dfObsSBTResp
    else:
        return None

# Recon Responses
configBQChoices = {
    "byVars": ["BookletNumber", "BlockCode"],
    "itemtypeColumn": "ItemTypeCode",
    "accnumColumn": "AccessionNumber",
    "outputColumn": "ReconstructedAnswer",
    "extInfoColumn": "extInfo",
    "maxNumberOfOptions": 10,
    "dispatcher": reconItemResponses,
    "postprocessor": postProcessObsBQChoicesResp,
    "handlers": {
        "BQChoices": reconBQChoice
    }
}
# Some MCSS items have options upto 63
configENAEP = {
    "byVars": ["BookletNumber", "BlockCode"],
    "itemtypeColumn": "ItemTypeCode",
    "accnumColumn": "AccessionNumber",
    "outputColumn": "ReconstructedAnswer",
    "extInfoColumn": "extInfo",
    "maxNumberOfOptions": 70,
    "dispatcher": reconItemResponses,
    "postprocessor": postProcessObsENAEPResp,
    "handlers": {
        "BQMCSS": reconMCSS,
        "BQMCMS": reconMCMS,
        "MCSS": reconMCSS,
        "MCMS": reconMCMS
    }
}
configSBT = {
    "byVars": ["BookletNumber", "BlockCode"],
    "itemtypeColumn": "Label",
#    "accnumColumn": "ControlId",
    "accnumColumn": "ResponseComponentId",
    "outputColumn": "ReconstructedAnswer",
    "extInfoColumn": "extInfo",
    "maxNumberOfOptions": 10,
    "dispatcher": reconSBTItemResponses,
    "postprocessor": postProcessObsSBTResp,
    "handlers": {
        "select.drop": reconSBTSelectDrop,
        "text.blur": reconSBTText,
        "select.choose": reconSBTSelectChoice
    }
}
configSBTTextSelectionResponses = {
    "byVars": ["BookletNumber", "BlockCode"],
    "itemtypeColumn": "Label",
#    "accnumColumn": "ControlId",
    "accnumColumn": "ResponseComponentId",
    "outputColumn": "ReconstructedAnswer",
    "extInfoColumn": "extInfo",
    "dispatcher": reconSBTItemResponses,
    "postprocessor": postProcessSBTTextSelectionResp,
    "handlers": {
        "select.toggle": reconSBTTextSelection
    }
}

# Extract responses
configChildItemType = {
    "itemtypeColumn": "ChildItemType",
    "responseColumn": "Response",
    "outputCol": "ExtractedAnswer",
    "handlers": {
        "MCMS": extractMCResponse,
        "MCSS": extractMCResponse,
        "Text": extractTextResponse,
        "Matching": extractMatchingtResponse,
        "TextSelection": extractTextSelectionResponse,
        "Selection": extractSelectionResponse
    }
}

configObsList = [configBQChoices, configENAEP, configSBT, configSBTTextSelectionResponses]
configRespList = [configChildItemType]

# to call,
# xvalBooklets(dfResp, dfObsResp,
#   configObsList=[configENAEP, configBQChoices, configSBT],
#   configRespList=[configChildItemType])

def xvalBooklets(dfResp, dfObsResp, configObsList, configRespList):
    """
    Cross-validates records for a booklet using data from a ready-made data frames. Returns a data frame containing
    extracted responses from the response data table and the reconstructed responses from the observable
    data, for selected item types that the x-val algorithm currently handles.

    :param dfResp: a data frame of response data, from which we extract the responses for each item
    :param dfObsResp: a data frame of observable data, from which we reconstruct responses for each item
    :param configObsList: list containing configurations for processing observables
    :param configRespList: list containing configurations for processing responses
    :return: a data frame that matches the extracted and reconstructed responses
    """

    assert (len(configObsList)>0 & ("itemtypeColumn" in configObsList))
    assert (isinstance(dfResp, pd.DataFrame))
    assert (isinstance(dfObsResp, pd.DataFrame))
    # make sure there are overlapping subjects
    subjlist = list(set(dfResp.BookletNumber.unique()).intersection(set(dfObsResp.BookletNumber.unique())))
    assert(len(subjlist)> 0)

    ##################
    # recon answers using the configObsList
    # Join the observable data back again

    try:
        dfObs = pd.concat([reconByConfig(dfObsResp, config=c) for c in configObsList])
        if dfObs.shape[0]>0:
            dfObs = dfObs.loc[:, ['BlockCode', 'BookletNumber', "AccessionNumber", 'ResponseComponentId',
                              'ReconstructedAnswer', 'ResponseHistory']]
    except Exception as e:
        logger.error("xvalBooklets: Error reconstructing responses")
        logger.exception(e)
        return None

    ##################
    # Merge recorded and reconstructed responses

    try:
        dfCompare = pd.merge(dfResp, dfObs, how="outer", on=["BookletNumber", "BlockCode", "ResponseComponentId"])
    except Exception as e:
        logger.error("xvalBooklets: Error merging response and observable data")
        logger.exception(e)
        return None

    # Need to transform the extracted responses by the `childItemType`, because `ItemTypeCode` is too gross.
    dfCompare.loc[dfCompare.ItemTypeCode.isin(["MCSS", "BQMCSS"]), "ChildItemType"] = "MCSS"
    dfCompare.loc[dfCompare.ItemTypeCode.isin(["MCMS", "BQMCMS"]), "ChildItemType"] = "MCMS"

    # ## Extract and transform responses to prepare for comparisons
    try:
        dfCompare = pd.concat([parseItemResponses(dfCompare, config=c) for c in configRespList])
    except Exception as e:
        logger.error("xvalBooklets: Error extracting responses")
        logger.exception(e)
        return None

    # ## Comparison and discrepancies

    # first, take care of a special case in BQMCMS and BQChoices, where one can add free text as "response"
    idx = dfCompare.ItemTypeCode.isin(["BQMCSS", "BQMCMS", "BQChoices"]) & dfCompare["ExtractedAnswer"].notnull()
    dfCompare.loc[idx, "ExtractedAnswer"] = dfCompare.loc[idx, "ExtractedAnswer"] \
        .apply(lambda l: [i for i in l if i not in ['response', 'response']])

    # discrepancies
    try:
        # we take a shortcut here, converting responses to a set of string-values
        # if the response is None, then the result is not a set, but a None
        setReconAnswer = dfCompare.loc[:, "ReconstructedAnswer"]\
            .apply(lambda respList: set([str(i) for i in respList]) if isinstance(respList,list) else None)
        setExtraAnswer = dfCompare.loc[:, "ExtractedAnswer"]\
            .apply(lambda respList: set([str(i) for i in respList]) if isinstance(respList,list) else None)

        dfCompare.loc[:, "matched"] = None
        # matched==True iff neither is None and the sets (of strings) are equal (recall None!=None)
        idx = setReconAnswer == setExtraAnswer
        dfCompare.loc[idx, "matched"] = True
        # matched==False iff the 2 sets were not equal, or one of them is None, but if both are None, we ignore
        idx = (setReconAnswer != setExtraAnswer)
        dfCompare.loc[idx, "matched"] = False
        dfCompare.loc[setReconAnswer.isnull() & setExtraAnswer.isnull(), "matched"] = None
        # if the response is empty, it is treated as missing; comparison is True
        idx = dfCompare["ReconstructedAnswer"].isnull() & (dfCompare["ExtractedAnswer"].apply(lambda l: l==[]))
#        dfCompare.loc[idx, "matched"] = None
        dfCompare.loc[idx, "matched"] = True
    except Exception as e:
        logger.error("xvalBooklets: Error comparing extracted and reconstructed responses")
        logger.exception(e)
        return None

    return dfCompare

