import json


def parseMatchMS(s):
    """
    Takes a JSON response from a matchMS item type, returns answers

    :param s: the json structure with responses
    :return: answer string
    """

    target = None
    source = None
    answerlist = []
    try:
        RespDict = json.loads(s)
        for element in RespDict:
            #print (type(element))
            for k,v in element.items():
                if(k=='source'):
                    source=v
                elif(k=='target'):
                    target=v
            answerlist.append("{}-{}".format(source, target))
    except:
        return None
    return answerlist