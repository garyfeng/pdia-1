import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode
from pdia.extendedInfoParser.parseJSON import parseJsonDatum


def parseTextChange(eInfo):
    """Parse First/Last text change from A,1 to Letter:A, """
    assert (isinstance(eInfo, pd.Series))
    try:
        section = eInfo.str.split(",").str.get(0)
        position = eInfo.str.split(",").str.get(1)
        res = [{"Part": s, "TextBox": p} for (s, p) in zip(section, position)]
    except:
        #        print "\nWarning: parseTextChange: some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res


def parseFocus(eInfo):
    """Return the focus events
    """

    def parseS2(s):
        if not isinstance(s, str):
            return None
        if (s.find(",") > 0):
            w = '{"Section":' + s.split(",")[0] + ',"Position":' + s.split(",")[1] + '}'
        else:
            if (s == 'None'):
                w = s
            else:
                w = '{"Position":' + s + '}'
        return w

    assert (isinstance(eInfo, pd.Series))
    # get rid of junk; restructure the JSON
    try:
        eInfo = eInfo.astype(str)
        res = eInfo.apply(parseS2)
    except:
        #        print "\nWarning: parseFocus: some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)

        # now return JSON/dict instead of a string(ified JSON)
    res = res.apply(parseJsonDatum)

    return res