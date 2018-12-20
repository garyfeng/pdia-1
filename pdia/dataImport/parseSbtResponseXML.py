import warnings
import json, re

import pandas as pd
from xml.etree import ElementTree as ET

from pdia import logger
from pdia.extendedInfoParser.parseXMLContentDatum import parseXMLContentDatum
from pdia.extendedInfoParser.parseJSONObservables import parseJSONObservables

def parseSbtResponseXML(source,bl="current",bc="current", unicodeJunkChar = "@"):#bl stands for bookletnumber; bc stands for blockcode
    """
    Parse the SBT xml string from SQL Response data table for each block and get Response Data.

    This function parses the XML string stored in the SQL Response Data Table for SBT and similar
    black-box component, where it keeps its own observable data and export
    an XML along with the response data. We have to export this data from
    the responseData SQL database as an XML file. This function takes an
    individual XML per student per block, and returns a Pandas data frame.

    :param source: the XML string or a XML node
    :param unicodeJunkChar: the character or string to replace any unicode characters; default to "@"
    :return: a data frame of response data or None if errors
    """

    # if source is a XML node, skip the parsing
    try:
        # first, replacing all unicode characters to unicodeJunkChar
        source = re.sub(r"\&\#x[0-9a-fA-F]+", unicodeJunkChar, source)
        # try to parse the xml string
        root = ET.fromstring(source)
    except Exception as e:
        #print bl, " " , bc, "Not able to parse"
        warnings.warn("BlockCode "+bc+" BookletNumber "+bl+" XML contains incomplete Booklet level information")
        logger.error("BlockCode "+bc+" BookletNumber "+bl+" XML contains incomplete Booklet level information")
        logger.exception(e)
        # not a string
        root = source

    responseList = []
    bookletDict = dict()
    # processing top-level xml elements
    try:
        bookletDict["BookletNumber"] = root.find("bookletId").text
        bookletDict["BlockCode"] = root.find("blockId").text
        bookletDict["ItemTypeCode"] = "SBT"
        bookletDict["AccessionNumber"] = root.find("taskId").text
    except Exception as e:
        #print bl, " ", bc, " error"
        warnings.warn("BlockCode "+bc+" BookletNumber "+bl+" XML contains incomplete Booklet level information")
        logger.error("BlockCode "+bc+" BookletNumber "+bl+" XML contains incomplete Booklet level information")
        logger.exception(e)
        return None

    # SBTs actually embed its own XML data, we need to loop through them and save each as a row
    for responseDatum in root.iter('responseDatum'):
        # make a copy of the itemDict
        respDict = bookletDict.copy()
        # populate
        respDict["SceneId"] = responseDatum.findtext('sceneId')
        respDict["responseComponentId"] = responseDatum.findtext('responseComponentId')
        respDict["responseType"] = responseDatum.findtext('responseType')
        # parse content
        content = responseDatum.find("content")
        ct = []
        if content is not None:
            for pair in content.iter('pair'):
                k = pair.find("key").text
                v = pair.find("value").text
                ct.append({"key": k, "val": v})
        respDict["Response"] = ct
        # add to the list
        responseList.append(respDict)
        # respDict.clear() # gc? No, stupid. This would clear the obj in the list already.

        # itemDict.clear() # gc? NO, see above.
    # error check
    # if no actual data records, exit with a warning and return None
    if len(responseList) == 0:
        #print bl," ",bc," has no data"
        warnings.warn("BlockCode "+bc+" BookletNumber "+bl+" XML contains no data")
        logger.warning("BlockCode "+bc+" BookletNumber "+bl+" XML contains no data")
        return None  # We have data. Now we create a data frame, parse the ExtendedInfo

    # notice the configuration is specified.
    try:
        df = pd.DataFrame.from_dict(responseList)
    except Exception as e:
        warnings.warn("XML data cannot be converted to a data frame")
        logger.error("XML data cannot be converted to a data frame")
        logger.exception(e)
        return None

    return df
