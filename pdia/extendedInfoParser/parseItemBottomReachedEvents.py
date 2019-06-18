import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode


def parseItemBottomReachedEvents(eInfo):
    """
    Parse event "Item Bottom Reached", which typically has value like
    "Block ID:888 Item ID:8888 Accession:VH888888"
    But there are also cases where the ExtendedInfo field is empty.

    :param eInfo: a Pandas Series (aka a list) of ExtendedInfo of the event
    :return: a JSON with parsed properties; None if empty
    """
    assert (isinstance(eInfo, pd.Series))

    def parseItemBottomString(s):
        if not isinstance(s, str): return None
        r = dict([ a.split(":") for a in s.replace(" ID", "ID").split(" ") ])
        return r

    try:
        res = eInfo.apply(parseItemBottomString)
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res
