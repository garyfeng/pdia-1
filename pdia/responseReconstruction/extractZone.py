import json


def parseZones(s):
    """
    Takes a json string for Zones item type, returns answers.

    :param s: the json structure with responses
    :return: answer string
    """
    try:
        RespDict = json.loads(s)
        return RespDict['Response']
    except:
        return None