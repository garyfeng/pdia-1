import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode


def parseEquationEditorEvents(eInfo):
    """ parse events """
    assert (isinstance(eInfo, pd.Series))
    try:
        res = eInfo.apply(lambda x: {"EquationEditorEvent": x})
    except:
        #        print "\nWarning: parseEquationEditorEvents: some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res


