import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode


def parseThemeEvents(eInfo):
    """Return the current theme as string

    The ExtendedInfo field contains a single string of the theme-changed-to.

    :param eInfo: a Pandas Series (aka a list) of ExtendedInfo of the event
    :return: a JSON with parsed properties
    """
    assert (isinstance(eInfo, pd.Series))
    try:
        # need to check the if x is a valid theme value
        res = eInfo.apply(lambda x: {"theme": x})
    except:
        #        print "\nWarning: parseThemeEvents: some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res