import json

from pdia.responseReconstruction.extractBQChoice import parseBQChoice
from pdia.responseReconstruction.extractMC import extractMC


def parseBlockReview(s):
    """
    extract responses from BlockReview events; for MC and GridMS items
    :param s: the json structure with responses
    :return: answer string
    """

    answerlist = []
    if (s.find('PartId') != -1):
        answerlist = parseBQChoice(s)
        return answerlist
    elif(s.find('"stateData"')!=-1):
        RespDict = json.loads(s)
        statedata = RespDict['stateData']
        answerlist.append(statedata['responseData'])
        return answerlist
    else:
        answerlist = extractMC(s)
        return answerlist
