import pandas as pd

from pdia.extendedInfoParser.parseJSON import parseJsonDatum


def parseThesaurus(eInfo):
    """Return thesaurus object
    """
    assert (isinstance(eInfo, pd.Series))
    try:
        res = eInfo.apply(parseJsonDatum)
    except:
        #        print "\nWarning: parseThesaurus(): blanks or non pd.Series"
        res = eInfo.apply(lambda x: "" if x is None else x)
    return res