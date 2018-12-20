import warnings
import pandas as pd
from xml.etree import ElementTree as ET

from pdia import logger
from pdia.extendedInfoParser.parseXMLContentDatum import parseXMLContentDatum
import unicodedata

def parseIctXML(source, keepResponseData=False):
    """
    Parse the 2015 ICT observables xml string for each block.

    The 2015 Science ICT follows a precursor of the SBT data format, where most of the
    observable events are saved in the Response data table, as a "response" associated
    with an AccNum. This function takes the XML string of that session, and returns a
    data frame following the standard format of the process data log.

    Note that there are several fields that are unused, e.g., "Label", because they
    are used in the eNAEP-based process data logs (which deal with response-related
    events). We need to merge the two sources of logs to obtain a complete proces
    data log.

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
        warnings.warn("ParseIctXML: XML contains incomplete Booklet level information")
        logger.error("ParseIctXML: XML contains incomplete Booklet level information")
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
        # get content in json format
        for content in observableDatum.iter('content'):
            # ct needs to be a string; but we will later re-parse this as JSON. @@@ Waste.
            # @@ why are we looping here? Shouldn't there be a single Content here?
            ct = unicodedata.normalize('NFKD', str(content.text))
            #ct = unicodeToAscii(content.text)

        observableMatrix.append({'BookletNumber': bookletId,
                                 'BlockId': blockId,
                                 'TaskId': taskId,
                                 'Accomodations': accommodations,
                                 'ExtendedTimeFactor': extendedTimeFactor,
                                 'SceneId': sceneId,
                                 'ControlId': controlId,
                                 'Label': eventType,
                                 'EventTime': timestamp,
                                 'ExtendedInfo': ct})

    # turn the data into a data frame
    if not keepResponseData:
        try:
            # create dataframe encapsules all the info
            # first create observable dataframe
            df = pd.DataFrame.from_dict(observableMatrix)
        except Exception as e:
            warnings.warn("ParseIctXML: cannot turn Observable XML into a data frame")
            logger.error("ParseIctXML: cannot turn Observable XML into a data frame")
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
                # TODO: We don't want to back-fill the response for each scene
                # If we ever do this, we want the ResponseContent to relfect the
                # state of the responses at this point.
                df = pd.merge(dfObs, dfResp, how='outer', on='SceneId')
        except Exception as e:
            warnings.warn("ParseIctXML: cannot turn XML into a data frame")
            logger.error("ParseIctXML: cannot turn XML into a data frame")
            logger.exception(e)
            return None

    return df


def ParseIctXML(source, keepResponseData=False):
    """Depreciated"""
    return parseIctXML(source, keepResponseData=False)
