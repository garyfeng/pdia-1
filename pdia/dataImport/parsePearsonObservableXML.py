from pdia.utils.logger import logger
import warnings
import re

import pandas as pd
from xml.etree import ElementTree as ET

from pdia.extendedInfoParser.parseExtendedInfo import parseExtendedInfo
from pdia.extendedInfoParser.parseXMLContentDatum import parseXMLContentDatum
from pdia.extendedInfoParser.parseJSONObservables import parseJSONObservables


def parsePearsonObservableXML(source, unicodeJunkChar = "@"):
    """
    Takes a Pearson observable XML string, returns a Pandas data frame.
    The Pearson XML export is one student per file, like the following:
    <?xml version="1.0" encoding="utf-8"?>
    <assessmentResult>
      <context>
        <sessionIdentifier sourceID="Database Version 213" softwareVersion="4.1.1.34969" superVersion="4.1.3" chromeExtension="3.1.3" assessmentYear="2017" schoolCode="666666" sessionNumber="DS0401" />
        <bookletNumber>8888888888</bookletNumber>
        <assignedForm>R888</assignedForm>
      </context>
      <testResult assessmentYear="2017" subjectName="Reading" assessedGroup="Grade 4" datestamp="2017-01-30T16:30:12.012Z">
        <outcomeVariable cardinality="record" interpretation="AdministrationCode">
          <value fieldIdentifier="AdministrationCode" baseType="integer">10</value>
          <value fieldIdentifier="AdministrationCodeDescription" baseType="string">Original session - In session full time</value>
        </outcomeVariable>
        <outcomeVariable cardinality="single" baseType="string" interpretation="TeacherNumber">
          <value>01</value>
        </outcomeVariable>
      </testResult>
      <itemResult accessionNumber="Adjust" itemType="Adjustment" blockCode="ADJUST">
        <outcomeVariable cardinality="single" interpretation="Enter Item">
          <value fieldIdentifier="EventTime" baseType="dateTime">2017-01-30T14:12:13.343Z</value>
        </outcomeVariable>
      </itemResult>
      ...
    Note that one or two of the <itemResult> elements may have ItemType=="SBT", such as
    <itemResult accessionNumber="VH888888" itemType="SBT" blockCode="8888888">
        <observableDatum>
          <sceneId>intro01</sceneId>
          <controlId>api</controlId>
          <eventType>api.itemReadyEvent</eventType>
          <timestamp>2017-12-11T14:29:12.531Z</timestamp>
          <content>
            <pair>
              <key>success</key>
              <value>true</value>
            </pair>
          </content>
        </observableDatum>
    In this case the function will unpack the SBT records as rows in the data frame as well. The code also replaces any unicode character with `@` by default.
    :param source: the XML string, or an XML root node
    :param unicodeJunkChar: the character or string to replace any unicode characters; default to "@"
    :return: a parsed Pandas data frame, or None if error
    """

    # if source is a XML node, skip the parsing

 #   print "From parsePearsonObservableXML"

    try:
        # first, replacing all unicode characters to unicodeJunkChar
        source = re.sub(r"\&\#x[0-9a-fA-F]+", unicodeJunkChar, source)
        # try to parse the xml string
        root = ET.fromstring(source)
    except Exception as e:
        warnings.warn("XML contains incomplete Booklet level information")
        logger.error("XML contains incomplete Booklet level information")
        logger.exception(e)
        # not a string
        root = source

    observableList = []
    bookletDict=dict()
    # processing top-level xml elements
    try:
        bookletDict["BookletNumber"]= root.find("context/bookletNumber").text
        bookletDict["Form"] = root.find("context/assignedForm").text
        bookletDict["SchoolCode"] = root.find("context/sessionIdentifier").get("schoolCode")
        bookletDict["sessionNumber"] = root.find("context/sessionIdentifier").get("sessionNumber")
        bookletDict["Year"] = root.find("context/sessionIdentifier").get("assessmentYear")
        bookletDict["Grade"] = root.find("testResult").get("assessedGroup")
        bookletDict["SubjectCode"] = root.find("testResult").get("subjectName")
    except Exception as e:
        warnings.warn("XML contains incomplete Booklet level information")
        logger.error("XML contains incomplete Booklet level information")
        logger.exception(e)
        return None

    for itemResult in root.iter("itemResult"):
        # make a copy of the bookletDict
        itemDict = bookletDict.copy()
        # populate
        itemDict["BlockCode"] = itemResult.get("blockCode")
        itemDict["ItemTypeCode"] = itemResult.get("itemType")
        itemDict["AccessionNumber"] = itemResult.get("accessionNumber")

        # Now depending on the itemType we have different processes
        if itemDict["ItemTypeCode"] in ["SBT", "ReadingNonSBT"]:
            # SBTs actually embed its own XML data, we need to loop through them and save each as a row
            for observableDatum in itemResult.iter('observableDatum'):
                # make a copy of the itemDict
                obsDict = itemDict.copy()
                # populate
                obsDict["SceneId"] = observableDatum.findtext('sceneId')
                obsDict["ControlId"] = observableDatum.findtext('controlId')
                obsDict["ResponseComponentId"] = observableDatum.findtext('controlId').rsplit('.',1)[0]
                obsDict["Label"] = observableDatum.findtext('eventType')
                obsDict["EventTime"] = observableDatum.findtext('timestamp')
                obsDict["ExtendedInfo"] = parseXMLContentDatum(observableDatum.find("content"))
                # add to the list
                observableList.append(obsDict)
                # obsDict.clear() # gc? No, stupid. This would clear the obj in the list already.
        else:
            # all others, each observableDatum is a row
            itemDict["Label"] = itemResult.find("outcomeVariable").get("interpretation")
            # populate
            for value in itemResult.find("outcomeVariable").iter("value"):
                itemDict[value.get("fieldIdentifier")] = value.text
            # add to the list
            observableList.append(itemDict)
        # itemDict.clear() # gc? NO, see above.
    # error check
    # if no actual data records, exit with a warning and return None
    if len(observableList) == 0:
        warnings.warn("XML contains no data")
        logger.warning("XML contains no data")
        return None  # We have data. Now we create a data frame, parse the ExtendedInfo

    # notice the configuration is specified.
    try:
        df = pd.DataFrame.from_dict(observableList)
        df = df.pipe(parseExtendedInfo)
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
