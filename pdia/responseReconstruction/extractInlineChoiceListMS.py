import json


def parseInlineChoiceListMS(s):
    """
    Takes a json response for InLineChoiceListMS item type, and returns answers.

    :param s: the json structure with responses
    :return: answer string
    """

    answerlist = []
    try:
        RespDict = json.loads(s)
        for records in RespDict["Response"]:
            answerlist.append("{}-{}".format(records["PartId"], records["Response"][0]))
    except:
        return None
    return answerlist
