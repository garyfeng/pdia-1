import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode
from pdia.extendedInfoParser.parseJSON import parseJsonDatum


def parseMediaEvents(eInfo):
    """
    Parse the media events

    Typical ExtendedInfo field looks like the following.

    # array(['AudioComplete', '{"Id":"1","PlayPause":"1"}',
    #   '{"Id":"1","ReachedEnd":"1"}', '{"Id":"1","PlayPause":"0"}',
    #   'AudioStarted', '{"Id":"1","Captions":"0"}',
    #   '{"Id":"1","Captions":"1"}'], dtype=object)

    :param eInfo: a pandas series of media related events
    :returns: a pandas series with parsed JSon, or dict; errorCode if errors.
    """

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
        res = eInfo.apply(lambda x: errorCode)
    return res


def parseMediaInteraction(eInfo):
    """
    Parse Media Interaction events.
    
    Media Interaction events in 2019 come in several flavors
    - a single string indicating the event, e.g., 'AudioComplete'
    - a concatenated string of media event and the MediaID/screen name, e.g., 'AudioStarted-ScrInt8'
    - a JSON-like string, like '{"Id":"1","PlayPause":"1"}'
    
    We will parse them all, and return a series of JSON/dict objects with 2 keys:
    - "MediaEvent": Play, Pause, CaptionsOn, CaptionsOff etc.
    - "MediaID": typically some code for the screen or item the media is in, and media part number. 
      We do not further interpret this; just pass along. When no info is given, we skip this key

    :param eInfo: a pandas series of media related events
    :returns: a pandas series with parsed JSon, or dict; errorCode if errors.
    """
    assert (isinstance(eInfo, pd.Series))
    
    def parseMediaString(s):
        """Takes "AudioStarted-ToolInt1", returns "{'mediaId':'ToolInt1', 'MediaEvent':'AudioStarted'}"
        """
        if not isinstance(s, str):
            return None
        slist = s.split("-")
        res = '{{"MediaEvent":"{}"}}'.format(slist[0]) if len(slist)==1 else \
            '{{"MediaID":"{}", "MediaEvent":"{}"}}'.format(slist[1], slist[0])
        return res
    
    try:
        idxJsonStr = eInfo.str.startswith("{")
        idxNonJsonStr = ~ eInfo.str.startswith("{")
        # get rid of junk; restructure the JSON
        eInfo[idxJsonStr] = eInfo[idxJsonStr] \
            .str.replace('"Id"', '"MediaID"') \
            .str.replace('"PlayPause":"1"', '"MediaEvent":"Play"') \
            .str.replace('"PlayPause":"0"', '"MediaEvent":"Paused"') \
            .str.replace('"ReachedEnd":"1"', '"MediaEvent":"ReachedEnd"') \
            .str.replace('"Captions":"0"', '"MediaEvent":"CaptionsOff"') \
            .str.replace('"Captions":"1"', '"MediaEvent":"CaptionsOn"')
        
        eInfo[idxNonJsonStr] = eInfo[idxNonJsonStr].apply(parseMediaString)
        
        res = eInfo.apply(parseJsonDatum)
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res
