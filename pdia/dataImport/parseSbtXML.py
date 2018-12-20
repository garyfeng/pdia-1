import warnings

import pandas as pd
from xml.etree import ElementTree as ET

from pdia import logger
from pdia.extendedInfoParser.parseXMLContentDatum import parseXMLContentDatum
from pdia.extendedInfoParser.parseJSON import parseJsonDatum


def parseSbtXML(source, keepResponseData = False):
    """
    Parse the SBT xml string for each block.
    The 2019 SBTs adds a new stateDiff field. This function takes an
    individual XML per student per block, and returns a Pandas data frame.
    
    :param source: the XML string or a XML node
    :param keepResponseData: false by default, otherwise combines both obs and res data.
    :return: a data frame or None
    """

    # if source is a XML node, skip the parsing
    try:
        parser = ET.XMLParser()
        root = ET.fromstring(source, parser=parser)
    except:
        # not a string
        root = source

    df = None
    # get top level basic info
    try:
        bookletId = root.findtext('bookletId')
        #    stateInfo=root.findtext('stateInfo')
        taskId = root.findtext('taskId')
        blockId = root.findtext('blockId')
        accommodations = root.findtext('accommodations')
        extendedTimeFactor = root.findtext('extendedTimeFactor')
        # print bookletId, taskId, blockId
    except Exception as e:
        warnings.warn("ParseSbtXML: XML contains incomplete Booklet level information")
        logger.error("ParseSbtXML: XML contains incomplete Booklet level information")
        logger.exception(e)
        return None

    # get observable data
    observableMatrix = []
    ct = None
    for observableDatum in root.iter('observableDatum'):
        sceneId = observableDatum.findtext('sceneId')
        controlId = observableDatum.findtext('controlId')
        eventType = observableDatum.findtext('eventType')
        timestamp = observableDatum.findtext('timestamp')
        stateDiff = observableDatum.findtext('stateDiff')
        # get content in json format
        for content in observableDatum.iter('content'):
            # ct needs to be a string; but we will later re-parse this as JSON. @@@ Waste.
            # @@ why are we looping here? Shouldn't there be a single Content here?
            ct = str(parseXMLContentDatum(content))

        observableMatrix.append({'BookletNumber': bookletId,
                                 'BlockId': blockId,
                                 'TaskId': taskId,
                                 'Accomodations': accommodations,
                                 'ExtendedTimeFactor': extendedTimeFactor,
                                 'SceneId': sceneId,
                                 'ControlId': controlId,
                                 'Label': eventType,
                                 'EventTime': timestamp,
                                 'StateDiff': stateDiff.replace("\n",""),
                                 'ExtendedInfo': ct})

    # turn the data into a data frame
    if not keepResponseData:
        try:
            # create dataframe encapsules all the info
            # first create observable dataframe
            df = pd.DataFrame.from_dict(observableMatrix)
        except Exception as e:
            warnings.warn("ParseSbtXML: cannot turn Observable XML into a data frame")
            logger.error("ParseSbtXML: cannot turn Observable XML into a data frame")
            logger.exception(e)
            return None

    else:
        # get response data
        responseMatrix = []
        ct = None
        for responseDatum in root.iter('responseDatum'):
            sceneId = responseDatum.findtext('sceneId')
            responseComponentId = responseDatum.findtext('responseComponentId')
            responseType = responseDatum.findtext('responseType')
            # get content in json format
            for content in responseDatum.iter('content'):
                # ct needs to be a string; but we will later re-parse this as JSON. @@@ Waste.
                # @@ why are we looping here? Shouldn't there be a single Content here?
                ct = str(parseXMLContentDatum(content))
            responseMatrix.append({'SceneId': sceneId,
                                   'ResponseComponentId': responseComponentId,
                                   'ResponseType': responseType,
                                   'ResponseContent': ct})

        try:
            # create dataframe encapsules all the info
            # first create observable dataframe
            dfObs = pd.DataFrame.from_dict(observableMatrix)
            # then create response dataframe
            dfResp = pd.DataFrame.from_dict(responseMatrix)
            if (dfResp.empty):
                df = dfObs
            elif (dfObs.empty):
                df = dfResp
            else:
                # GF: Wait, does "outer" really work here?
                df = pd.merge(dfObs, dfResp, how='outer', on='SceneId')
        except Exception as e:
                warnings.warn("ParseSbtXML: cannot turn XML into a data frame")
                logger.error("ParseSbtXML: cannot turn XML into a data frame")
                logger.exception(e)
                return None

    return df

def getStateInfo(source):
    """
    Extract the <stateInfo> field, which should be a JSON.
    
    :param source: the XML string or a XML node
    :return: the json parsed as dict
    """

    # if source is a XML node, skip the parsing
    try:
        parser = ET.XMLParser()
        root = ET.fromstring(source, parser=parser)
    except:
        # not a string
        root = source
    # get top level basic info
    try:
        stateInfo=root.findtext('stateInfo')
    except:
        return {}
    
    res = parseJsonDatum(stateInfo)
    return res
