from pdia.utils.logger import logger
import warnings

import pandas as pd
# from lxml import etree
from xml.etree import ElementTree as ET

from pdia.extendedInfoParser.parseMathML import parseMathML
from pdia.extendedInfoParser.parseExtendedInfo import parseExtendedInfo
from pdia.extendedInfoParser.parseXMLContentDatum import parseXMLContentDatum

def parsePearsonObservableXML(source):
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

    :param source: the XML string, or an XML root node
    :return: a parsed Pandas data frame, or None if error
    """

    # if source is a XML node, skip the parsing
    try:
        parser = ET.XMLParser()
        root = ET.fromstring(source, parser=parser)
    except:
        # not a string
        root = source

    df = None
    observableMatrix = []
    # processing top-level xml elements
    try:
        context = root.find("context")
        sessionID = context.find("sessionIdentifier")
        sessionNumber = sessionID.attrib["sessionNumber"]
        bookletNumber = context.findtext("bookletNumber")
        schoolCode = sessionID.attrib["schoolCode"]
        assessmentYear = sessionID.attrib["assessmentYear"]
        assignedForm = context.findtext("assignedForm")
        #    chromeExtension=sessionID.attrib["chromeExtension"]
        #    superVersion=sessionID.attrib["superVersion"]
        #    softwareVersion=sessionID.attrib["softwareVersion"]
        #    sourceID=sessionID.attrib["sourceID"]
        testResult = root.find("testResult")
        #   datestamp = testResult.attrib["datestamp"]
        assessedGroup = testResult.attrib["assessedGroup"]
        subjectName = testResult.attrib["subjectName"]
        # logging
        logger.debug("Booklet: %s, %s, %s, %s, %s, %s",
                     subjectName, sessionNumber, schoolCode,
                     assessmentYear, bookletNumber, assignedForm)
        # print subjectName, sessionNumber, schoolCode, assessmentYear, bookletNumber, assignedForm
        #   for outcome in testResult.iter("outcomeVariables"):
        #       for value in outcome.iter("value"):
        #           if(value.attrib["fieldIdentifier"]=="AdministrationCode"):
        #               AdministrationCode=value.text
        #           elif(value.attrib["fieldIdentifier"]=="AdministrationCodeDescription"):
        #               AdministrationCodeDescription=value.text
        #           elif(value.attrib["fieldIdentifier"]=="TeacherNumber"):
        #               TeacherNumber=value.text
    except Exception as e:
        warnings.warn("XML contains incomplete Booklet level information")
        logger.error("XML contains incomplete Booklet level information")
        logger.exception(e)
        return None

    ct = None
    for itemResult in root.iter("itemResult"):
        blockCode = itemResult.attrib["blockCode"]
        itemType = itemResult.attrib["itemType"]
        accessionNumber = itemResult.attrib["accessionNumber"]

        # Now depending on the itemType we have different processes

        if (itemType == "SBT"):
            # SBTs actually embed its own XML data,
            # we need to loop through them and save each as a row
            for observableDatum in root.iter('observableDatum'):
                sceneId = observableDatum.findtext('sceneId')
                controlId = observableDatum.findtext('controlId')
                eventType = observableDatum.findtext('eventType')
                timestamp = observableDatum.findtext('timestamp')
                for content in observableDatum.iter('content'):
                    # ct needs to be a string; but we will later re-parse this as JSON. @@@ Waste.
                    # @@ why are we looping here? Shouldn't there be a single Content here?
                    ct = str(parseXMLContentDatum(content))

                observableMatrix.append({"BookletNumber": bookletNumber,
                                         "AssignedForm": assignedForm,
                                         "SessionNumber": sessionNumber,
                                         "SchoolCode": schoolCode,
                                         "AssessmentYear": assessmentYear,
                                         "Grade": assessedGroup,
                                         "Subject": subjectName,
                                         "BlockCode": blockCode,
                                         "ItemType": itemType,
                                         "AccessionNumber": accessionNumber,
                                         "SceneId": sceneId,
                                         "controlId": controlId,
                                         "Label": eventType,
                                         "EventTime": timestamp,
                                         "ExtendedInfo": ct})
        else:
            # all others, each observableDatum is a row
            outcomeVar = itemResult.find("outcomeVariable")
            label = outcomeVar.attrib["interpretation"]
            extendedInfo = ""
            eventTime = ""
            for value in outcomeVar.iter("value"):
                if (value.attrib["fieldIdentifier"] == "EventTime"):
                    eventTime = value.text
                elif (value.attrib["fieldIdentifier"] == "ExtendedInfo"):
                    extInf = value.text
                    # for math we remove the MathML because it's too large
                    # we keep only the latex
                    if (subjectName == "Mathematics" and label == "Math Keypress"):
                        extendedInfo = parseMathML(extInf)
                    else:
                        extendedInfo = extInf

            observableMatrix.append({"BookletNumber": bookletNumber,
                                     "SessionNumber": sessionNumber,
                                     "SchoolCode": schoolCode,
                                     "AssessmentYear": assessmentYear,
                                     "Grade": assessedGroup,
                                     "Subject": subjectName,
                                     "BlockCode": blockCode,
                                     "ItemType": itemType,
                                     "AccessionNumber": accessionNumber,
                                     "Label": label,
                                     "EventTime": eventTime,
                                     "ExtendedInfo": extendedInfo})
    # error check
    # if no actual data records, exit with a warning and return None
    if len(observableMatrix) == 0:
        warnings.warn("XML contains no data")
        logger.warning("XML contains no data")
        return None  # We have data. Now we create a data frame, parse the ExtendedInfo

    # notice the configuration is specified.
    try:
        df = pd.DataFrame.from_dict(observableMatrix)
        df = df.pipe(parseExtendedInfo)
        df = df.sort_values("EventTime")
    except Exception as e:
        warnings.warn("XML data cannot be converted to a data frame")
        logger.error("XML data cannot be converted to a data frame")
        logger.exception(e)
        return None

    # if(eventTime<>""):
    #        df=df.sort_values("EventTime")
    return df

def ParsePearsonObservableXML(source):
    """Depreciated"""
    return parsePearsonObservableXML(source)
