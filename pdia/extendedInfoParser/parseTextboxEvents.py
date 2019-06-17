import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode
from pdia.extendedInfoParser.parseJSON import parseJsonDatum


def parseTextChange(eInfo):
    """Parse First/Last text change from A,1 to {"ItemPart":"A", "TextBox":"1"}. Deprecated because we now use
    Differential Keystroke Logging events to capture all keypresses.
    
    :param eInfo: a Pandas Series (aka a list) of ExtendedInfo of the event
    :return: a JSON with parsed properties; None if empty
    """
    assert (isinstance(eInfo, pd.Series))
    try:
        section = eInfo.str.split(",").str.get(0)
        position = eInfo.str.split(",").str.get(1)
        res = [{"ItemPart": s, "TextBox": p} for (s, p) in zip(section, position)]
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res


def parseFocus(eInfo):
    """Parse "Receive Focus" and "Loose Focus" events. Typical ExtendedInfo field is like
    "Part B, 1", or simply '1'. We will return something like: {"ItemPart":"B", "TextBox":"1"}
    
    :param eInfo: a Pandas Series (aka a list) of ExtendedInfo of the event
    :return: a JSON with parsed properties; None if empty
    """

    def parseFucusString(s):
        """"Parse "Receive Focus" and "Loose Focus" events. Typical ExtendedInfo field is like
        "Part B, 1", or simply '1'. We will return something like: {"ItemPart":"B", "TextBox":1}
        """
        if not isinstance(s, str):
            return None
        data = s.split(", ")
        if len(data)==1:
            r = {"TextBox":"{}".format(data[0])}
        elif len(data)==2:
            r = {"ItemPart":"{}".format(data[0]), "TextBox":"{}".format(data[1])}
        else:
            # something is wrong
            r = errorCode
        return r

    assert (isinstance(eInfo, pd.Series))
    # get rid of junk; restructure the JSON
    try:
        eInfo = eInfo.astype(str)
        res = eInfo.apply(parseFucusString)
    except:
        res = eInfo.apply(lambda x: errorCode)

    return res