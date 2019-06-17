import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode


def parseTTSEvents(eInfo):
    """Return the Text-to-speech events

    ExtendedInfo in TTS events is typically a string of the following kind:
    - "TextToSpeech Mode On"
    - "TextToSpeech Mode Off"
    - "TextToSpeech Mode Read: Scale one. Scale two. ..."

    We return:
    - {"TTS":"On"}, {"TTS":"Off"}
    - {"TTSRead":"..."}

    :param eInfo: a Pandas series containing ExtendedInfo events
    :return: a parsed series of JSON/DICT objects, or errorCode if error    
    """
    # there are 3 kinds of events:
    # TextToSpeech Read: TextToSpeechMode On
    # TextToSpeech Read: TextToSpeechMode Off
    # TextToSpeech Read: The actual text being read...
    assert (isinstance(eInfo, pd.Series))

    def parseTTSString(s):
        if not isinstance(s, str): return None
        if s == "TextToSpeech Mode On": return {"TTS":"On"}
        if s == "TextToSpeech Mode Off": return {"TTS":"Off"}
        return {"TTSRead":"{}".format(s.replace("TextToSpeech Read: ", ""))}

    try:
        # need to check the format first
        res = eInfo.apply(parseTTSString)
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res