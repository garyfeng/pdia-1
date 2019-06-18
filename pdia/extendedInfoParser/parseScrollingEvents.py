import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode


def parseItemScrollEvents(eInfo):
    """
    Parse event "item scroll", which typically has value like
    "100, right, mouse/trackpad, main, 0, 60"

    :param eInfo: a Pandas Series (aka a list) of ExtendedInfo of the event
    :return: a JSON with parsed properties
    """
    # 100, right, mouse/trackpad, main, 0, 60
    assert (isinstance(eInfo, pd.Series))
    try:
        parsed = eInfo.str.split(",[ ]*")
        res = [{"zoomLevel": z,
                "ScrollDirection": d,
                "ScrollMethod": m,
                "ScrollArea": a,
                "ScrollPixelsY": v,
                "ScrollPixelsX": h
                } for (z, d, m, a, v, h) in parsed]
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res

