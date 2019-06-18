import re
import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode
from pdia.extendedInfoParser.parseJSON import parseJsonDatum

# # Scratchwork
# "Scratchwork Mode On": parseNameValuePairs,
# "Scratchwork Highlight Mode On": parseNameValuePairs,
# "Clear Scratchwork": parseNameValuePairs,
# "Scratchwork Mode Off": parseNameValuePairs,
# "Scratchwork Draw Mode Off": parseNameValuePairs,
# "Scratchwork Draw Mode On": parseNameValuePairs,
# "Scratchwork Erase Mode On": parseNameValuePairs,
# "Scratchwork Erase Mode Off": parseNameValuePairs,
# "Scratchwork Highlight Mode Off": parseNameValuePairs,
# # "Draw": parseNameValuePairs,
# # "Erase": parseNameValuePairs,
# # "Highlight": parseNameValuePairs,

# Scratchwork overlay
def parseScratchworkModeOnEvents(eInfo):
    """ parse Scratchwork Mode On events 

    We will simply return something like
    {"ScratchworkOverlay":"On", 
     "ScratchworkDrawMode":"On",
     "ScratchworkEraseMode":"Off",
     "ScratchworkHighlightMode":"Off"
    }

    :param eInfo: a Pandas series containing ExtendedInfo events
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """
    assert (isinstance(eInfo, pd.Series))

    try:
        res = eInfo.apply(lambda x: {"ScratchworkOverlay":"On", 
            "ScratchworkDrawMode":"On",
            "ScratchworkEraseMode":"Off",
            "ScratchworkHighlightMode":"Off"
            })
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res

def parseScratchworkModeOffEvents(eInfo):
    """ parse Scratchwork Mode Off events 

    We will simply return something like
    {"ScratchworkOverlay":"Off", 
     "ScratchworkDrawMode":"Off",
     "ScratchworkEraseMode":"Off",
     "ScratchworkHighlightMode":"Off"
    }
    :param eInfo: a Pandas series containing ExtendedInfo events
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """
    assert (isinstance(eInfo, pd.Series))

    try:
        res = eInfo.apply(lambda x: {"ScratchworkOverlay":"Off", 
            "ScratchworkDrawMode":"Off",
            "ScratchworkEraseMode":"Off",
            "ScratchworkHighlightMode":"Off"
            })
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res

# Draw Mode
def parseScratchworkDrawModeOnEvents(eInfo):
    """ parse Scratchwork Draw Mode On events 

    We will simply return something like

    {"ScratchworkDrawMode":"On",
    "ScratchworkEraseMode":"Off",
    "ScratchworkHighlightMode":"Off"}

    Note that the draw, eraser, and highight functions are multually exclusive.

    :param eInfo: a Pandas series containing ExtendedInfo events
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """
    assert (isinstance(eInfo, pd.Series))

    try:
        res = eInfo.apply(lambda x: {"ScratchworkDrawMode":"On",
            "ScratchworkEraseMode":"Off",
            "ScratchworkHighlightMode":"Off"})
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res

def parseScratchworkDrawModeOffEvents(eInfo):
    """ parse Scratchwork Draw Mode Off events 

    We will simply return something like
    {"ScratchworkDrawMode":"Off"}

    We know it is turned off, but we don't know which mode is on instead.

    :param eInfo: a Pandas series containing ExtendedInfo events
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """
    assert (isinstance(eInfo, pd.Series))

    try:
        res = eInfo.apply(lambda x: {"ScratchworkDrawMode":"Off"})
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res

# Erase Mode
def parseScratchworkEraseModeOnEvents(eInfo):
    """ parse Scratchwork Erase Mode On events 

    We will simply return something like the following:

    {"ScratchworkDrawMode":"Off",
    "ScratchworkEraseMode":"On",
    "ScratchworkHighlightMode":"Off"}

    Note that the draw, eraser, and highight functions are multually exclusive.

    :param eInfo: a Pandas series containing ExtendedInfo events
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """
    assert (isinstance(eInfo, pd.Series))

    try:
        res = eInfo.apply(lambda x: {"ScratchworkDrawMode":"Off",
            "ScratchworkEraseMode":"On",
            "ScratchworkHighlightMode":"Off"})
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res

def parseScratchworkEraseModeOffEvents(eInfo):
    """ parse Scratchwork Erase Mode Off events 

    We will simply return something like
    {"ScratchworkEraseMode":"Off"}

    We know it is turned off, but we don't know which mode is on instead.

    :param eInfo: a Pandas series containing ExtendedInfo events
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """
    assert (isinstance(eInfo, pd.Series))

    try:
        res = eInfo.apply(lambda x: {"ScratchworkEraseMode":"Off"})
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res

# Highlight Mode
def parseScratchworkHighlightModeOnEvents(eInfo):
    """ parse Scratchwork Highlight Mode On events 

    We will simply return something like the following:
    
    {"ScratchworkDrawMode":"Off",
    "ScratchworkEraseMode":"Off",
    "ScratchworkHighlightMode":"On"}

    Note that the draw, eraser, and highight functions are multually exclusive.

    :param eInfo: a Pandas series containing ExtendedInfo events
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """
    assert (isinstance(eInfo, pd.Series))

    try:
        res = eInfo.apply(lambda x: {"ScratchworkDrawMode":"Off",
            "ScratchworkEraseMode":"Off",
            "ScratchworkHighlightMode":"On"})
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res

def parseScratchworkHighlightModeOffEvents(eInfo):
    """ parse Scratchwork Highlight Mode Off events 

    We will simply return something like
    {"ScratchworkHighlightMode":"Off"}

    We know it is turned off, but we don't know which mode is on instead.

    :param eInfo: a Pandas series containing ExtendedInfo events
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """
    assert (isinstance(eInfo, pd.Series))

    try:
        res = eInfo.apply(lambda x: {"ScratchworkHighlightMode":"Off"})
    except:
        res = eInfo.apply(lambda x: errorCode)
    return res

