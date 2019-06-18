import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode
from pdia.extendedInfoParser.parseJSON import parseJsonDatum

def parseIICObservables(eInfo):
    """Parse IIC Observables ExtendedInfo field, returns a parsed JSON of states.

    The process data from Interactive Item Components (IICs) is an array with the following fields:
    - a: an integer typically 140~149; an id but with no obvious significance
    - t: the UTC timestamp as string
    - state: an arbitrary JSON object specific to an IIC, with keys such as
        - a: an integer typically 140~149; this should be identical with the 'a' field above
        - t: the UTC timestamp as string that should be the same as 't' above; sometimes this is missing
        - s: the state, which is an arbitrary JSON object specific to an IIC. 

    For example:
    [
        140,
        '2019-03-01T15:46:06.303Z',
        {'a': 140,
         's': '[{"ParamName":"version","Value":"5.13"},{"ParamName":"nativeWidth","Value":"1200"},...}]'
        }
    ]

    or 

    [
        141,
        '2019-03-01T15:46:15.894Z',
        {
            'a': 141,
            's': {
                'stateSavedFlag': '1',
                'savedPosX': 600,
                'savedPosY': 200,
                'savedAngle': 0,
                'savedTheme': 'high'
            },
            't': '2019-03-01T15:46:15.894Z'
        }
    ]

    We will parse these as a valid JSON object, and flatten them into 

    {"a":"xxx", "t":"yyy", "s_x1":1, "s_x2":2, ...}

    :param eInfo: a Pandas series of ExtendedInfo for IIC Observable events
    :returns: a series of parsed, flattened JSON/dict, or errorCode
    """

    assert (isinstance(eInfo, pd.Series))
    
    def makeKeyValuePairs(s):
        """ given something like
        '[{"ParamName":"version","Value":"5.14"},{"ParamName":"nativeWidth","Value":"1000"},...'
        return {"version":"5.14", "nativeWidth":"1000", ...}
        """
        data = parseJsonDatum(s, flatten=False)
        res = dict()
        for kv in data:
            res[kv["ParamName"]] = kv["Value"]
        return res
    
    def parseIICString(x):
        data = parseJsonDatum("["+str(x)+"]", flatten=False)
        try:
            res = data[2]
            res["t"] = data[1]
            if isinstance(res["s"], str) and res["s"].startswith('[{"ParamName"'):
                res["s"] = makeKeyValuePairs(res["s"])
        except KeyError:
            return errorCode
        except IndexError:
            return errorCode
        return flatten_dict(res)
        
    try:
        res = eInfo.apply(lambda x: parseIICString(x))
    except:
        #        print "\nWarning: parseCalculatorEvents(): some rows of ExtendedInfo is not a string"
        #        return parseDefault(eInfo)
        return eInfo.apply(lambda x: errorCode)
    return res