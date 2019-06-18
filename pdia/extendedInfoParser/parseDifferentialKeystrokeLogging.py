import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode
from pdia.extendedInfoParser.parseJSON import parseJsonDatum

def parseDifferentialKeystrokeLogging(eInfo):
    """Parse differential keystroke logging events in CR items.

    The log looks like:
        [1551453019752,1,"C","\"\""]	
    which contains:
    - timestamp in epoch format
    - position of editing action
    - string to insert
    - string to delete; always insert before delete

    We return the following structure
    {"t":xxx, "KeystrokePosition": xxx, "KeystrokeInsStr":xxx, 
    "KeystrokeDelStr":xxx}

    Note that in the original coding, an empty string for insertion or deletion
    becomes `'""'` after conversion. This is wrong; it's meant to be `''`. We fixed
    this.

    :param eInfo: a pandas series of the extendefInfo for the keylogs
    :returns: a series of parsed events; or errorCode
    """
    assert (isinstance(eInfo, pd.Series))
    
    def parseKeyLog(s):
        try:
            data = parseJsonDatum(s, flatten=False)
            r = {
                "t": str(pd.to_datetime(data[0],unit='ms')),
                "KeystrokePosition": data[1],
                "KeystrokeInsStr": data[2].replace('""', ''),
                "KeystrokeDelStr": data[3].replace('""', ''),
                  }
        except:
            return errorCode
        return r
    
    try:
        res = eInfo.apply(parseKeyLog)
    except:
        return eInfo.apply(lambda x: errorCode)
    return res
