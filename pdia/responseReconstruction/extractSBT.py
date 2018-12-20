import string

from lxml import etree

from pdia.extendedInfoParser.parseXMLContentDatum import parseXMLContentDatum
from pdia.responseReconstruction.extractMathML import MathMLExtraction


def extractSBT(s):
    """
    Takes a string of the SBT XML, and returns the answers of the SBT.

    :param s: the json structure with responses
    :return: answer string
    """

    if(s.find('<responseData>') > 0 and s.find('</responseData>' )== -1):
        if(s.rfind('</responseDatum>') >0):
            s=s.rsplit('</responseDatum>',1)[0]+'</responseDatum></responseData>'
        else:
            s = s+'</responseData>'

    s = str(s, errors='ignore')
    root = etree.fromstring(s)

    answerlist = []
    for responseDatum in root.iter('responseDatum'):
        sceneId = responseDatum.findtext('sceneId')
        responseComponentId=responseDatum.findtext('responseComponentId')
        responseType = responseDatum.findtext('responseType')
        for content in responseDatum.iter('content'):
            ctdict = parseXMLContentDatum(content)
            if(responseType=="Selection"):
                for key, value in ctdict.items():
                    if(value == 'true'):
                        sel = string.ascii_uppercase[key]
                        answerlist.append("{}-{}".format(responseComponentId, sel))
                        break
            elif(responseType=="TextSelection"):
                for key, value in ctdict.items():
                    answerlist.append("{}-{}".format(responseComponentId, value))
            elif(responseType == "Math"):
                #mathml, output last action
                for key, value in ctdict.items():
                    val = MathMLExtraction(value)
                    answerlist.append("{}-{}".format(key, val))
            elif (responseType == "Text"):
                for key, value in ctdict.items():
                    if(value.startswith('![CDATA[')):
                        value = value.split('![CDATA[')[1].rstrip(']]')
                    answerlist.append("{}-{}".format(key, value))
            elif(responseType == "Record"):
                for key, value in ctdict.items():
                    answerlist.append("{}-{}".format(key, value))
            else:
                continue
    return answerlist