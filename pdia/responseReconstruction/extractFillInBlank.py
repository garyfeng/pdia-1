import json

from pdia.responseReconstruction.extractMathML import MathMLExtraction


def parseFillInBlank(s):
    """
    Takes a json string for responses for FillInBlank item types; returns answers

    :param s: the json structure with responses
    :return: answer string
    """

    answerlist=[]
    try:
        RespDict = json.loads(s)
        for records in RespDict["Response"]:
            if (records['Response'].find('<math xmlns=')!=-1):
                val=MathMLExtraction(records['Response'])
                answerlist.append("{}-{}".format(records["PartId"],val))
            else:
                val=records['Response']
                answerlist.append(val)
    except:
        return None
    return answerlist