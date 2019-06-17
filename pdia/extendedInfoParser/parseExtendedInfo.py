import pandas as pd

errorCode = {"Error": "ParsingError"}

from pdia.extendedInfoParser.parseCalculatorEvents import parseCalculatorEvents, \
    parseCalculatorBuffer
from pdia.extendedInfoParser.parseClickChoiceEvents import parseClearAnswerEvents, parseClickChoiceEvents
from pdia.extendedInfoParser.parseClickProgressEvents import parseClickProgressEvents
from pdia.extendedInfoParser.parseDropChoiceEvents import parseDropChoice
from pdia.extendedInfoParser.parseDifferentialKeystrokeLogging import parseDifferentialKeystrokeLogging
from pdia.extendedInfoParser.parseEquationEditorEvents import \
    parseEquationEditorEvents, parseEquationEditorButtonEvents, parseMathKeypressEvents,\
    parseCloseEquationEditorEvents, parseOpenEquationEditorEvents
from pdia.extendedInfoParser.parseIICObservables import parseIICObservables
from pdia.extendedInfoParser.parseJSONObservables import parseJSONObservables
from pdia.extendedInfoParser.parseYesNo import parseYesNo
from pdia.extendedInfoParser.parseKeyValuePairs import parseNameValuePairs
from pdia.extendedInfoParser.parseMediaEvents import parseMediaInteraction
from pdia.extendedInfoParser.parseReadingPassageEvents import parsePassageEvents
from pdia.extendedInfoParser.parseScrollingEvents import parseItemScrollEvents
from pdia.extendedInfoParser.parseItemBottomReachedEvents import parseItemBottomReachedEvents
from pdia.extendedInfoParser.parseTTSEvents import parseTTSEvents
from pdia.extendedInfoParser.parseTextboxEvents import parseTextChange, parseFocus
from pdia.extendedInfoParser.parseThemeEvents import parseThemeEvents
from pdia.extendedInfoParser.parseWritingEvents import parseThesaurus
from pdia.extendedInfoParser.parseZoomEvents import parseZoomEvents

def parseDefault(eInfo):
    """Return None for each element; use as a catch-all
    """
    assert (isinstance(eInfo, pd.Series))
    eInfo.loc[:] = None
    return eInfo


# # Parsing ExtendedInfo
#
# The `ExtendedInfo` field contain structured or semi-structured data about certain events,
# albeit in a string format. In order to access the data, we need to turn them into Python objects.
# Or more precisely, Pandas Series of Python objects.
#
# In the case where the `ExtendedInfo` is stored in JSON, life is easy (assuming it's valid). For other
# cases, we write little parsers to convert info into objects.
#
# **Note that the function `parseExtendedInfo()` will by design set the output column to `None`. **
# If you plan to parse certain subsets of events incrementally, make sure to use the individual
# parser functions or develop your own. They will return Pandas Series which you can assign your data frame.
#
def parseExtendedInfo(df,
                      config=None,
                      extInfo="ExtendedInfo",
                      outInfo="extInfo",
                      label="Label"):
    """Parse the ExtendedInfo field, return a df with parsed ExtendedInfo in the "extInfo" field

    According to the 2015/16 NAEP Observable protocols, the "ExtendedInfo" field contains additional
    information encoded in idiosyncratic formats, depending on the event type as indexed by "Label".
    This function aims to decode these, and return the df with an additional column of outInfo.

    :param df: the input data frame
    :type df: Pandas data frame

    :param config: optional configuation object; default to None
    :type config: object or None

    :param extInfo: optional, column name for ExtendedInfo
    :type extInfo: string

    :param outInfo: optional, name of the output column that contains the parsed extInfo. If equals to
        extInfo, it will overwrite the ExtendedInfo column with parsed version. In parsing failes, it
        is set to None ~~copies the extInfo, i.e., as a string~~.
    :type outInfo: string

    :param label: optional, name of the column indicating the event type, which determines how to parse.
    :type outInfo: string

    :returns: df with outInfo and errInfo
    :rtype: Pandas data frame

    """

    assert (isinstance(df, pd.DataFrame))
    assert (extInfo in df.columns)
    assert (label in df.columns)

    if config is None:
        config = {
            "handlers": {
                # No extended info
                # "Enter Item": parseDefault,
                # "Exit Item": parseDefault,
                # "Next": parseDefault,
                # "Back": parseDefault,
                # 'Display Reminder': parseDefault,
                # 'Application Recovery': parseDefault,
                # "Leave Section": parseDefault,
                # "Show Timer": parseDefault,
                # "Hide Timer": parseDefault

                # common eNAEP events
                "OK": parseYesNo,
                "None": parseDropChoice,
                'Horizontal Item Scroll': parseItemScrollEvents,
                'Vertical Item Scroll': parseItemScrollEvents,
                'Item Bottom Reached': parseItemBottomReachedEvents,
                "nothing": parseDefault,
                "Yes": parseYesNo,
                "No": parseYesNo,
                "Lose Focus": parseFocus,
                "Receive Focus": parseFocus,
                "Click Progress Navigator": parseClickProgressEvents,
                "Media Interaction": parseMediaInteraction,

                # Universal Design tools
                'Increase Zoom': parseZoomEvents,
                'Decrease Zoom': parseZoomEvents,
                "Change Theme": parseThemeEvents,
                "TextToSpeech": parseTTSEvents,

                # Scratchwork
                "Scratchwork Mode On": parseNameValuePairs,
                "Scratchwork Highlight Mode On": parseNameValuePairs,
                "Clear Scratchwork": parseNameValuePairs,
                "Scratchwork Mode Off": parseNameValuePairs,
                "Scratchwork Draw Mode Off": parseNameValuePairs,
                "Scratchwork Draw Mode On": parseNameValuePairs,
                "Scratchwork Erase Mode On": parseNameValuePairs,
                "Scratchwork Erase Mode Off": parseNameValuePairs,
                "Scratchwork Highlight Mode Off": parseNameValuePairs,
                "Draw": parseNameValuePairs,
                "Erase": parseNameValuePairs,
                "Highlight": parseNameValuePairs,

                # common item responses
                "DropChoice": parseDropChoice,
                "Click Choice": parseClickChoiceEvents,
                "Eliminate Choice": parseClickChoiceEvents,
                "Clear Answer": parseClearAnswerEvents,
                "Text Entered": parseTextChange,
                # "First Text Change": parseTextChange,
                # "Last Text Change": parseTextChange,
                "Differential Keystroke Logging": parseDifferentialKeystrokeLogging,
                "IIC Observables": parseIICObservables,

                # Math
                "Open Calculator": parseCalculatorEvents,
                "Close Calculator": parseCalculatorEvents,
                "Move Calculator": parseCalculatorEvents,
                "Calculator Buffer": parseCalculatorBuffer,
                "Calculator Keystroke Logging": parseCalculatorKeystrokeLoggingEvents,
                "Open Equation Editor": parseOpenEquationEditorEvents,
                "Close Equation Editor": parseCloseEquationEditorEvents,
                "Equation Editor Button": parseEquationEditorButtonEvents,
                "Math Keypress": parseMathKeypressEvents,

                # Reading
                "Activate Footnoter": parseNameValuePairs,
                "Dismiss Footnoter": parseNameValuePairs,
                "Next Passage Page Swipe": parsePassageEvents,
                "Previous Passage Page Swipe": parsePassageEvents,
                "Other Passage Page": parsePassageEvents,
                "Next Passage Page": parsePassageEvents,
                "Previous Passage Page": parsePassageEvents,
                "Click Passage Tab": parsePassageEvents,
                "Show Questions Panel": parseNameValuePairs,
                "Hide Questions Panel": parseNameValuePairs,
                "Click Look-back Button": parseNameValuePairs,

                # Writing
                "Pilot Observables": parseJSONObservables,
                "Keypress": parseJSONObservables,
                "Misspellings Corrected": parseJSONObservables,
                "Misspellings Identified": parseJSONObservables,
                "RightClick Misspellings": parseJSONObservables,
                "Thesaurus Replacement": parseJSONObservables,
                "Menu Thesaurus": parseThesaurus,
            }
        }

    # now let's revert the config, to get `parser:[list of labels]`
    funcMap = {}
    for k, v in config["handlers"].items():
        funcMap[v] = funcMap.get(v, []) + [k]

    # clear outInfo
    df.loc[:, outInfo] = None
    # we now loop through all funcMap elements and do the conversion
    for parser, eventList in funcMap.items():
        idx = df.loc[:, label].isin(eventList)
        # df.loc[idx,outInfo]=np.where((df.loc[idx, extInfo]==errorCode),\
        # df.loc[idx,"ExtendedInfo"],parser(df.loc[idx, extInfo]))
        df.loc[idx, outInfo] = parser(df.loc[idx, extInfo])
    return df
