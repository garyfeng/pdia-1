import json

from pdia.responseReconstruction.extractMathML import MathMLExtraction


def parseExtendedText(s):
    """
    Takes a string with responses to ExtendedText item type, returns a list of answers.
    Will extract MathML answers.

    :param s: the json structure with responses
    :return: answer string
    """

    answerlist = []
    try:
        RespDict = json.loads(s)
        if (RespDict["Response"]):
            if (RespDict["Response"][0].find("<math xmlns=") != -1):  # mathml
                val = MathMLExtraction(RespDict["Response"][0])
                answerlist.append(val)
            else:
                answerlist.append(RespDict["Response"][0].lstrip('[').rstrip(']'))
    except:
        return None
    return answerlist
