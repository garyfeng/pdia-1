import json


def parseGridMS(s):
    """
    Takes a string of JSON response to a gridMS item type; returns answers

    :param s: the json structure with responses
    :return: answer string
    """
    answerlist = []
    thisId = None

    try:
        RespDict = json.loads(s)
        for items in RespDict["Response"]:
            for key, value in items.items():
                if(key=='GroupId' or key=='PartId'):
                    thisId = value
                    #print (type(value))
                if (key == 'Response'):
                    for element in value:
                        for k, v in element.items():
                            if (k == 'Selected' and v is True):
                                # print(id, element['val'])
                                if (element['val'] != ''):
                                    value = element['val']
                                else:
                                    value = None
                                answerlist.append("{}-{}".format(thisId, value))
    except:
        return None
    return answerlist
