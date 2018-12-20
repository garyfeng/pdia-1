import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode

def parseCalculatorEvents(eInfo):
    """Parse a calculator event string, return parsed object or None
    """
    assert (isinstance(eInfo, pd.Series))
    try:
        res = eInfo.apply(lambda x: {"Calculator": x})
    except:
        #        print "\nWarning: parseCalculatorEvents(): some rows of ExtendedInfo is not a string"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res


def parseCalculatorBuffer(eInfo):
    """Parse a calculator buffer string, return parsed object or None
    """
    assert (isinstance(eInfo, pd.Series))
    try:
        res = eInfo.apply(lambda x: {"CalculatorBuffer": x})
    except:
        #        print "\nWarning: parseCalculatorBuffer(): some rows of ExtendedInfo is not a string"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res