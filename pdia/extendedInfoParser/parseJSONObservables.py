import pandas as pd

from pdia.extendedInfoParser.parseJSON import parseJsonDatum


def parseJSONObservables(eInfo):
    """Parse a JSON-based pd series, return parsed objects
    """
    assert (isinstance(eInfo, pd.Series))

    # return eInfo.apply(lambda x: parseJsonDatum(x))
    # lambda is about 20% slower than no-lambda
    return eInfo.apply(parseJsonDatum)