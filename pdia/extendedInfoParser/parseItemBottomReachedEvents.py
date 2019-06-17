import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode


def parseItemBottomReachedEvents(eInfo):
    """
    Parse event "Item Bottom Reached", which typically has value like
    "Block ID:888 Item ID:8888 Accession:VH888888"
    But there are also cases where the ExtendedInfo field is empty

    :param eInfo: a Pandas Series (aka a list) of ExtendedInfo of the event
    :return: a JSON with parsed properties; None if empty
    """
    assert (isinstance(eInfo, pd.Series))
    try:
        if eInfo.isnan():
            return eInfo.apply(lambda x: None)

        eInfo = eInfo.str.replace(" ID", "ID")
        parsed = eInfo.str.split("[ :]")
        res = [{"BlockID": x2,
                "ItemID": x4,
                "Accession": x6
                } for (x1, x2, x3, x4, x5, x6) in parsed]
    except:
        #        print "\nWarning: parseItemScrollEvents(): some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res
