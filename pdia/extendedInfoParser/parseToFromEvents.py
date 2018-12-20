import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode


def parseToFromColumn(eInfo):
    """Parse To/From type columns in format 'to, from'. """
    assert (isinstance(eInfo, pd.Series))

    # parse the fromVal and toVal & put together
    try:
        fromTab = eInfo.str.split(",[ ]*").str.get(0)
        toTab = eInfo.str.split(",[ ]*").str.get(1)
        res = [{"from": f, "to": t} for (f, t) in zip(fromTab, toTab)]
    except:
        #       print "\nWarning: parseToFromColumn(): some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return