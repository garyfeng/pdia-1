import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode
from pdia.extendedInfoParser.parseJSON import parseJsonDatum


def parseNameValuePairs(eInfo):
    """Parse general name value pairs"""

    def parseString(s):
        if not isinstance(s, str):
            return None
        if (s.find(":") > 0):
            w = '{"' + s.split(":")[0] + '":"' + s.split(":")[1] + '"}'
        else:
            if (s == 'NaN' or s == '' or s == 'None'):
                w = None
            else:
                ### need to modify, add a label or something to make it pair
                w = '{' + s + '}'
        return w

    assert (isinstance(eInfo, pd.Series))
    try:
        res = eInfo.apply(parseString)
    except:
        #        print "\nWarning: parseNameValuePairs: some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)

        # now return JSON/dict instead of a string(ified JSON)
    res = res.apply(parseJsonDatum)

    return res