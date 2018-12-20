import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode
from pdia.extendedInfoParser.parseJSON import parseJsonDatum


def parsePassageEvents(eInfo):
    """parse reading previous/next passage etc. event extended info"""

    def parseStr(s):
        if not isinstance(s, str):
            return None
        if (s.find(",") > 0):
            w = '{"From":' + s.split(",")[0] + ',"To":' + s.split(",")[1] + '}'
        else:
            if (s == 'None' or s == 'NaN' or s == ''):
                w = None
            else:
                ### need to modify, add a label or something to make it a pair
                w = '{' + s + '}'
        return w

    assert (isinstance(eInfo, pd.Series))
    try:
        res = eInfo.apply(parseStr)
    except:
        res = eInfo.apply(lambda x: errorCode)

        # now return JSON/dict instead of a string(ified JSON)
    res = res.apply(parseJsonDatum)

    return res