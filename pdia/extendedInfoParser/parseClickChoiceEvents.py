import re
import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode
from pdia.extendedInfoParser.parseJSON import parseJsonDatum

def parseClickChoiceEvents(eInfo):
    """ parse Click Choice and Eliminate Choice events 

    The ExtendedInfo contains a string like "VH854750A-2:checked", in which case we will return
    {"AccNum":"VH854750", "ItemPart": "A", "ItemOption":"2", "OptionStatus":"checked"}

    :param eInfo: a Pandas series containing ExtendedInfo events
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """
    assert (isinstance(eInfo, pd.Series))

    def parseChoiceString(s):
        res = re.match('(VH[0-9]+)([A-Z]*)-([0-9]+):([a-z]+)', s)
        if res is None: return None
        # turn this into a dict
        try:
            r = dict([(a, b) for a, b in \
                zip(["AccNum", "ItemPart", "ItemOption", "OptionStatus"],\
                res.groups())])
        except:
            return None
        return r

    try:
        res = eInfo.apply(parseChoiceString)
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res


def parseClearAnswerEvents(eInfo):
    """ parse Clear Answer events 

    The ExtendedInfo is either 'NaN' or a string like 'Part A'.

    :param eInfo: a Pandas series containing ExtendedInfo events
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """
    assert (isinstance(eInfo, pd.Series))

    def parseClearAnswerString(s):
        r = s.replace("Part ", "") if isinstance(s, str) else ""
        return {"ItemPart": "{}".format(r), "OptionStatus":"cleared"}

    try:
        res = eInfo.apply(parseClearAnswerString)
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res    