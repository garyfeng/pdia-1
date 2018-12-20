import json

# BQNumeric
sBQNumeric = """{'Response': [{'PartId': '1', 'Response': '4'}]}"""


def parseBQNumeric(s):
    """
    takes a string with response JSON, and returns the BQNumeric resposnes as an array of arrays.
    Each BQNumeric will have a single response.

    :param s: the json structure with responses
    :return: answer string

    """

    answerlist = []
    try:
        RespDict = json.loads(s)
        for records in RespDict["Response"]:
            answerlist.append(records["Response"])
    except:
        return None
    return answerlist
