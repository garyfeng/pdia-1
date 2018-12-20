import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode


def parseClickEvents(eInfo):
    """ parse events """
    assert (isinstance(eInfo, pd.Series))
    try:
        res = eInfo.apply(lambda x: {"ClickProgress": x})
    except:
        #        print "\nWarning: parseClickEvents: some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res