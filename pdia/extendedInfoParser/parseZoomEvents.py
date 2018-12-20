import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode

def parseZoomEvents(eInfo):
    """Return zoom level objects, with zoomLevel as int
    """
    #        Label                EventTime ExtendedInfo        date
    # 761  Decrease Zoom  2016-02-02 15:01:08.070          100  2016-02-02
    assert (isinstance(eInfo, pd.Series))
    try:
        res = eInfo.apply(lambda x: {"zoomLevel": int(x)})
    except:
        #        print "\nWarning: parseZoomEvents: some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res