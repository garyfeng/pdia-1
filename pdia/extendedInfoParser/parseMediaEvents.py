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
    Parse Media Interaction events.
    
    Media Interaction events in 2019 come in several flavors
    - a single string indicating the event, e.g., 'AudioComplete'
    - a concatenated string of media event and the mediaID/screen name, e.g., 'AudioStarted-ScrInt8'
    - a JSON-like string, like '{"Id":"1","PlayPause":"1"}'
    
    We will parse them all, and return a series of JSON/dict objects with 2 keys:
    - "mediaEvent": Play, Pause, CaptionsOn, CaptionsOff etc.
    - "mediaID": typically some code for the screen or item the media is in, and media part number. 
      We do not further interpret this; just pass along. When no info is given, we skip this key

    :param eInfo: a pandas series of media related events
    :returns: a pandas series with parsed JSon, or dict; errorCode if errors.
    """
    # array(['AudioComplete', '{"Id":"1","PlayPause":"1"}',
    #   '{"Id":"1","ReachedEnd":"1"}', '{"Id":"1","PlayPause":"0"}',
    #   'AudioStarted', '{"Id":"1","Captions":"0"}',
    #   '{"Id":"1","Captions":"1"}',
    #   'AudioStarted-ScrInt8', 'AudioComplete-ScrInt8'
    # ], dtype=object)

    assert (isinstance(eInfo, pd.Series))
    
    def parseMediaString(s):
        """Takes "AudioStarted-ToolInt1", returns "{'mediaId':'ToolInt1', 'mediaEvent':'AudioStarted'}"
        """
        if not isinstance(s, str):
            return None
        slist = s.split("-")
        res = '{{"mediaEvent":"{}"}}'.format(slist[0]) if len(slist)==1 else \
            '{{"mediaID":"{}", "mediaEvent":"{}"}}'.format(slist[1], slist[0])
        return res
    
    try:
        idxJsonStr = eInfo.str.startswith("{")
        idxNonJsonStr = ~ eInfo.str.startswith("{")
        # get rid of junk; restructure the JSON
        eInfo[idxJsonStr] = eInfo[idxJsonStr] \
            .str.replace('"Id"', '"mediaID"') \
            .str.replace('"PlayPause":"1"', '"mediaEvent":"Play"') \
            .str.replace('"PlayPause":"0"', '"mediaEvent":"Paused"') \
            .str.replace('"ReachedEnd":"1"', '"mediaEvent":"ReachedEnd"') \
            .str.replace('"Captions":"0"', '"mediaEvent":"CaptionsOff"') \
            .str.replace('"Captions":"1"', '"mediaEvent":"CaptionsOn"')
        
        eInfo[idxNonJsonStr] = eInfo[idxNonJsonStr].apply(parseMediaString)
        
        res = eInfo.apply(parseJsonDatum)
    except:
        #        print "\nWarning: parseMediaEvents: some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res
    