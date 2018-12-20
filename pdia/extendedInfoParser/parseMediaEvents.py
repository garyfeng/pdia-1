import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode
from pdia.extendedInfoParser.parseJSON import parseJsonDatum


def parseMediaEvents(eInfo):
    """
    Parse the media events

    :param eInfo: a pandas series of media related events
    :returns: a pandas series with parsed JSon, or dict; errorCode if errors.
    """
    # array(['AudioComplete', '{"Id":"1","PlayPause":"1"}',
    #   '{"Id":"1","ReachedEnd":"1"}', '{"Id":"1","PlayPause":"0"}',
    #   'AudioStarted', '{"Id":"1","Captions":"0"}',
    #   '{"Id":"1","Captions":"1"}'], dtype=object)

    assert (isinstance(eInfo, pd.Series))
    try:
        # get rid of junk; restructure the JSON
        eInfo = eInfo.str.replace("AudioComplete", '{"Id":"1", "event":"AudioComplete"}') \
            .str.replace("AudioStarted", '{"Id":"1","event":"AudioStarted"}') \
            .str.replace('"PlayPause":"1"', '"event":"Play"') \
            .str.replace('"PlayPause":"0"', '"event":"Paused"') \
            .str.replace('"ReachedEnd":"1"', '"event":"ReachedEnd"') \
            .str.replace('"Captions":"0"', '"event":"CaptionsOff"') \
            .str.replace('"Captions":"1"', '"event":"CaptionsOn"')
        res = eInfo.apply(parseJsonDatum)
    except:
        #        print "\nWarning: parseMediaEvents: some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res


def parseMediaInteraction(eInfo):
    """
    Return the media interaction events.

    There are two formats, one is JSON and the other
    a "-"-delimited string. We deal with them separately, using `mask`.

    :param eInfo: a pandas series of media related events
    :returns: a pandas series with parsed JSon, or dict; errorCode if errors.
    """

    def parseS1(s):
        if not isinstance(s, str):
            return None
        if (s.find("-") > 0):
            w = '{"Id":1, "event":' + s.split("-")[0] + ', "target":' + s.split("-")[1] + '}'
        else:
            w = '{"Id":1, "event":' + s + ', "target": nan }'
        return w

    assert (isinstance(eInfo, pd.Series))
    # get rid of junk; restructure the JSON
    try:
        res = eInfo
        eInfo = eInfo.astype(str)
        mask = eInfo.str.startswith('{')
        s2 = eInfo[mask]
        res.loc[mask] = s2.str.replace('"PlayPause":"1"', '"event":"Play","target":"NaN"') \
            .str.replace('"PlayPause":"0"', '"event":"Paused","target":"NaN"') \
            .str.replace('"ReachedEnd":"1"', '"event":"ReachedEnd","target":"NaN"') \
            .str.replace('"Captions":"0"', '"event":"CaptionsOff","target":"NaN"') \
            .str.replace('"Captions":"1"', '"event":"CaptionsOn","target":"NaN"')
        res.loc[~mask] = eInfo[~mask].apply(parseS1)
    except:
        #        print "\nWarning: parseMediaInteration: some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)

    # now return JSON/dict instead of a string(ified JSON)
    res = res.apply(parseJsonDatum)

    return res
