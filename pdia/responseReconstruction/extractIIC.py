import json


def parseInteractive(s):
    """
    Takes the json response from an IIC item, returns the answer

    :param s: the json structure with responses
    :return: answer string
    """

    answerlist = []
    try:
        RespDict = json.loads(s)
        if(type(RespDict['responseData'])==list):
            response=','.join(RespDict['responseData'])
        else:
            response=RespDict['responseData']
        answerlist.append(response)
    except:
        return None
    return answerlist
