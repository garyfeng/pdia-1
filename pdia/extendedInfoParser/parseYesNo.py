import pandas as pd
from pdia.extendedInfoParser.parseExtendedInfo import errorCode
from pdia.extendedInfoParser.parseJSON import parseJsonDatum


def parseYesNo(eInfo):
    """Parse Yes/No events

    Yes/No events are responses to a dialogue box. It can have different formats:

    Example: {u'Event': u'EOSTimeLeft', u'Language': u' ENG'}
    or: "SQNoAnswer, en-US"

    We will have to deal with them individually and then parse using parseJSON.

    :param eInfo: a Pandas Series (aka a list) of ExtendedInfo of the event
    :return: a JSON with parsed properties; None if empty
    """
    assert (isinstance(eInfo, pd.Series))

    def parseYN(s):
        if not isinstance(s, str): 
            return None
        try:
            if s.startswith("{"):
                # JSON format
                r = parseJsonDatum(s)
            else:
                # string, assuming comma delimited
                data = s.split(", ")
                r = {"Event": data[0], "Language", data[1]}
        except:
            r = errorCode
        return r


    try:
        res = eInfo.apply(parseYN)
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res
