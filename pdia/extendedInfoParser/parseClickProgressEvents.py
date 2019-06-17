import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode


def parseClickProgressEvents(eInfo):
    """ parse Click Progress Bar events 

    The ExtendedInfo returns a single numeric value, the percentage of completedness.

    :param eInfo: a Pandas series containing ExtendedInfo events
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """
    assert (isinstance(eInfo, pd.Series))
    try:
        res = eInfo.apply(lambda x: {"ProgressBar": x})
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res