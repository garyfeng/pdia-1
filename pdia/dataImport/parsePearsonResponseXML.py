import pandas as pd
from xml.etree import ElementTree as ET

from pdia import logger


def extractSbtResponseXML(itemResult, headerDict):
    """Given a XML node "itemResult", return a list of responses

    :param itemResult: a xml.etree node that is itemResult
    :param headerDict: a dictionary with student-level information such as teh BookletNumber, etc.
    :returns: a list of dicts or None
    """
    responseMatrix = []
    try:
        blockCode = itemResult.get("blockCode")
        itemAccessionNumber = itemResult.get("accessionNumber")
        # sometimes response data is stored under a different AccNum than the ItemAccNum
        accessionNumber = itemResult.get("respondedIn")
        if not accessionNumber:
            accessionNumber = itemAccessionNumber

        itemType = itemResult.get("itemType")

        # we need to loop through responseDatum elements
        responseData = itemResult.find('responseVariable/candidateResponse/value/taskState/responseData')
        for responseDatum in responseData.iter('responseDatum'):
            sceneId = responseDatum.find("sceneId").text
            responseComponentId = responseDatum.find("responseComponentId").text
            responseType = responseDatum.find("responseType").text

            content = responseDatum.find("content")
            ct = []
            if content is not None:
                for pair in content.iter('pair'):
                    k = pair.find("key").text
                    v = pair.find("value").text
                    ct.append({"key": k, "val": v})

            responseMatrix.append({
                'BookletNumber': headerDict['BookletNumber'],
                'Form': headerDict['Form'],
                'Year': headerDict['Year'],
                'SubjectCode': headerDict['SubjectCode'],
                'Grade': headerDict['Grade'],
                'BlockCode': blockCode,
                'AccessionNumber': accessionNumber,
                'ItemAccessionNumber': itemAccessionNumber,
                'ItemTypeCode': itemType,
                'ChildItemAccessionNumber': sceneId,
                'ChildItemType': responseType,
                'ResponseComponentId': responseComponentId,
                'Response': ct
            })
    except Exception as e:
        logger.error("extractSbtResponseXML: Error parsing the SBT XML itemResult")
        logger.exception(e)
        return None

    return responseMatrix


def parsePearsonResponseXML(source):
    """
    Parse Pearson response XMLs, using XPath.

    Naming following the SQL::

        [ItemResponse].[ItemResponseId],
        Subject.SubjectCode,
        Assessment.AssessedGroupId as Grade,
        Student.BookletNumber,
        [Block].BlockCode,
        Item.AccessionNumber,
        ItemType.ItemTypeCode,
        [ItemResponse].[Response],
        [ItemResponse].[IsAnswered]

    We are adding a few new columns:

    - ``ChildItemAccessionNumber``: native for some eNAEP; for SBT type::

        'ChildItemAccessionNumber': sceneId

    - ``ChildItemType``: native for some eNAEP; for SBT type::

        'ChildItemType': responseType

    - ``ResponseComponentId``: native for SBT style data; for eNAEP, it is a combination of AccNum and childAccNum::

        'ResponseComponentId': "item-{}".format(accessionNumber)\\
                if childItemAccessionNumber is None else\\
                "item-{}-{}".format(accessionNumber, childItemAccessionNumber),


    :param source: the XML string or a XML node
    :return: a data frame or None
    """

    # if source is a XML node, skip the parsing
    try:
        root = ET.fromstring(source)
    except:
        # not a string
        root = source

    # get top level basic info, using proper xpath
    try:
        bookletNumber = root.find('./context/bookletNumber').text
        assignedForm = root.find('./context/assignedForm').text
        assessmentYear = root.find('./testResult').get("assessmentYear")
        subjectName = root.find('./testResult').get("subjectName")
        grade = root.find('./testResult').get("assessedGroup")
    except Exception as e:
        logger.error("parseResponseXML: XML contains incomplete Booklet level information")
        logger.exception(e)
        return None

    responseMatrix = []
    headerDict = {
        'BookletNumber': bookletNumber,
        'Form': assignedForm,
        'Year': assessmentYear,
        'SubjectCode': subjectName,
        'Grade': grade}

    for itemResult in root.iter('itemResult'):

        # now the key/value pairs
        if itemResult.get("itemType") in ["SBT", "ReadingNonSBT"]:
            try:
                responseMatrix += extractSbtResponseXML(itemResult, headerDict)
            except Exception as e:
                logger.error("parseResponseXML: Unable to parse SBT responseData")
                logger.exception(e)
                continue
        else:
            # regular eNAEP types
            try:
                blockCode = itemResult.get("blockCode")
                itemAccessionNumber = itemResult.get("accessionNumber")
                # sometimes response data is stored under a different AccNum than the ItemAccNum
                accessionNumber = itemResult.get("respondedIn")
                if not accessionNumber:
                    accessionNumber = itemAccessionNumber
                itemType = itemResult.get("itemType")
                childItemAccessionNumber = itemResult.get("childItemAccessionNumber")
                childItemType = itemResult.get("childItemType")
                content = itemResult.find("responseVariable/candidateResponse/value/content")
                ct = []
                if content is not None:
                    for pair in content.iter('pair'):
                        k = pair.find("key").text
                        v = pair.find("value").text
                        ct.append({"key": k, "val": v})

                responseMatrix.append({
                    'BookletNumber': bookletNumber,
                    'Form': assignedForm,
                    'Year': assessmentYear,
                    'SubjectCode': subjectName,
                    'Grade': grade,
                    'BlockCode': blockCode,
                    'AccessionNumber': accessionNumber,
                    'ItemAccessionNumber': itemAccessionNumber,
                    'ItemTypeCode': itemType,
                    'ChildItemAccessionNumber': childItemAccessionNumber,
                    'ChildItemType': childItemType,
                    'ResponseComponentId': "item-{}".format(accessionNumber) \
                        if childItemAccessionNumber is None else \
                        "item-{}-{}".format(accessionNumber, childItemAccessionNumber),
                    'Response': ct
                })
            except Exception as e:
                logger.error("parseResponseXML: Unable to parse eNAEP response content")
                logger.exception(e)
                continue

    return pd.DataFrame(responseMatrix)
