import json

from pdia.responseReconstruction.extractBQChoice import parseBQChoice
from pdia.responseReconstruction.extractMC import extractMC
from pdia.responseReconstruction.extractSBT import extractSBT


def parseDialog(s):
    """
    Takes a string with JSON of responses for Dialog events, returns the answer string.
    Deals with SBT, MCMS and ExtendedText subtypes

    :param s: the json structure with responses
    :return: answer string
    """

    # combination of SBT, MCMS and ExtendedText
    # print ('In Dialog')
    answerlist = []
    if (s.find('<responseData>') !=-1):
        #same as SBT
        answerlist=extractSBT(s)
        return answerlist
    elif(s.find('PartId') !=-1):
        answerlist=parseBQChoice(s)
        return answerlist
    elif(s.find('Selected')!=-1):
        answerlist= extractMC(s)
        return answerlist
    else:
        try:
            RespDict = json.loads(s)
            answerlist.append(RespDict['Response'])
            return answerlist
        except:
            return None