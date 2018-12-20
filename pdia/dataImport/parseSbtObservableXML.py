import warnings
import json, re

import pandas as pd
from xml.etree import ElementTree as ET

from pdia import logger
from pdia.extendedInfoParser.parseXMLContentDatum import parseXMLContentDatum
from pdia.extendedInfoParser.parseJSONObservables import parseJSONObservables

def parseSbtObservableXML(source, bl="current",bc="current", unicodeJunkChar = "@"):#bl stands for bookletnumber; bc stands for blockcode
    """
    Parse the SBT xml string from SQL Response data table for each block to get Observable data frame.

    This function parses the XML string stored in the SQL Response Data Table for SBT and similar
    black-box component, where it keeps its own observable data and export
    an XML along with the response data. We have to export this data from
    the responseData SQL database as an XML file. This function takes an
    individual XML per student per block, and returns a Pandas data frame.

    :param source: the XML string or a XML node
    :param unicodeJunkChar: the character or string to replace any unicode characters; default to "@"
    :return: a data frame of observables or None if errors
    """
    # if source is a XML node, skip the parsing

    print('From parseSbtobservableXML')

    try:
        # first, replacing all unicode characters to unicodeJunkChar
        source = re.sub(r"\&\#x[0-9a-fA-F]+", unicodeJunkChar, source)
        # try to parse the xml string
        root = ET.fromstring(source)
    except Exception as e:
        #print bl, " ", bc, "Not able to parse"
        warnings.warn("BlockCode "+bc+" BookletNumber "+bl+" XML contains incomplete Booklet level information")
        logger.error("BlockCode "+bc+" BookletNumber "+bl+" XML contains incomplete Booklet level information")
        logger.exception(e)
        # not a string
        root = source
    observableList = []
    bookletDict = dict()
    # processing top-level xml elements
    try:
        bookletDict["BookletNumber"] = root.find("bookletId").text
        # bookletDict["Form"] = ""
        # bookletDict["SchoolCode"] = ""
        # bookletDict["sessionNumber"] = ""
        # bookletDict["Year"] = ""
        # bookletDict["Grade"] = ""
        # bookletDict["SubjectCode"] = ""
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
    for observableDatum in root.iter('observableDatum'):

        # make a copy of the itemDict
        obsDict = bookletDict.copy()
        # populate
        obsDict["SceneId"] = observableDatum.findtext('sceneId')
        obsDict["ControlId"] = observableDatum.findtext('controlId')

#        obsDict["ResponseComponentId"]=observableDatum.findtext('controlId').rsplit('.',1)[0]

        obsDict["Label"] = observableDatum.findtext('eventType')
        obsDict["EventTime"] = observableDatum.findtext('timestamp')
        obsDict["ExtendedInfo"] = parseXMLContentDatum(observableDatum.find("content"))
        # add to the list
        observableList.append(obsDict)
        # obsDict.clear() # gc? No, stupid. This would clear the obj in the list already.

        # itemDict.clear() # gc? NO, see above.
    # error check
    # if no actual data records, exit with a warning and return None
    if len(observableList) == 0:
        #print bl," ",bc," has no data"
        warnings.warn("BlockCode "+bc+" BookletNumber "+bl+" XML contains no data")
        logger.warning("BlockCode "+bc+" BookletNumber "+bl+" XML contains no data")
        return None  # We have data. Now we create a data frame, parse the ExtendedInfo
    # notice the configuration is specified.
    try:
        df = pd.DataFrame.from_dict(observableList)
        # parse extended info for SBT items
        idx = df["ItemTypeCode"].isin(["SBT", "ReadingNonSbt"])
        df.loc[idx, "extInfo"] = df.loc[idx, "ExtendedInfo"].pipe(parseJSONObservables)
        df = df.sort_values("EventTime")
    except Exception as e:
        warnings.warn("XML data cannot be converted to a data frame")
        logger.error("XML data cannot be converted to a data frame")
        logger.exception(e)
        return None
    return df
