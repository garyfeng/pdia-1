import json

from pdia.responseReconstruction.extractBQChoice import parseBQChoice
from pdia.responseReconstruction.extractMC import extractMC


def extractBQNotAnswered(s):
    """
    Takes a json string for responses for SQNotAnswered item type; returns the answer.

    :param s: the json structure with responses
    :return: answer string
    """

    answerlist = []
    if(s.find('PartId') != -1):

        answerlist = parseBQChoice(s)
        return answerlist
    elif(s.find('Selected') != -1):

        answerlist = extractMC(s)
        return answerlist
    else:

        try:
            RespDict = json.loads(s)
            answerlist.append(RespDict['Response'])
            return answerlist
        except:
            return None
    return None
