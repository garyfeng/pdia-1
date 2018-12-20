import json
import warnings

from pdia.responseReconstruction.extractMathML import MathMLExtraction


def parseComposite(s):
    """
    Takes a string with responses from a Composite item type; returns the answer string

    :param s: the json structure with responses
    :return: answer string
    """

    answerlist = []
    try:
        RespDict = json.loads(s)
    except:
        return None
    for records in RespDict["Response"]:
        if('Type' in records):
            for record in records["Response"]:
                if(record is None):
                    continue
                if(records['Type'] == 'T'):
                    if (record["Selected"] is True):
                        if (record['val'].find("<math") != -1):
                            value = MathMLExtraction(record["val"])
                        else:
                            value=record['val']
                        answerlist.append("{}-{}".format(records["PartId"], value))
                elif(records['Type'] == 'MATCHMS'):#MatchMS
                    value="{}-{}".format(record['source'], record['target'])
                    answerlist.append("{}-{}".format(records["PartId"], value))
                elif(records['Type']=='MCSS' or records['Type'] == 'MCMS' or records['Type'] == 'MAPMS' or
                             records['Type'] == 'MAPSS' or records['Type'] == 'InlineChoices'):
                    #MAPMS and MAPSS look the same as MCMS and MCSS
                    if (record["Selected"] is  True):
                        if (record["val"] == ""):
                            value='X'
                        else:
                            value=record["val"]
                        answerlist.append("{}-{}".format(records["PartId"], value))
        else:
            warnings.warn("Type is missing for Part ID", records['PartId'])
            continue
    return answerlist
