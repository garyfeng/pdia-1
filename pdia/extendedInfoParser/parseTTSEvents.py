import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode


def parseTTSEvents(eInfo):
    """Return the Text-to-speech events
    """
    # there are 3 kinds of events:
    # TextToSpeech Read: TextToSpeechMode On
    # TextToSpeech Read: TextToSpeechMode Off
    # TextToSpeech Read: The actual text being read...
    assert (isinstance(eInfo, pd.Series))
    # get rid of junk
    try:
        # need to check the format first
        eInfo = eInfo.str.replace("TextToSpeech Read: ", "").str.replace("TextToSpeechMode ", "")
        res = eInfo.apply(lambda x: {"TTS": x})
    # return the content, or "On" or "Off"
    except:
        #        print "\nWarning: parseTTSEvents: some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res