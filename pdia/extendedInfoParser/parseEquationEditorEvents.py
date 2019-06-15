import pandas as pd

from pdia.extendedInfoParser.parseExtendedInfo import errorCode
from pdia.extendedInfoParser.parseJSON import parseJsonDatum

# A sample of equation editor action sequences from 2019 NAEP Mathematics
# Receive Focus,1/3/2019 03:31:50.835 PM,1
# Math Keypress,1/3/2019 03:31:58.978 PM,"{""numericIdentifier"":""1"",""partId"":"""",""contentMathML"":""<math xmlns=\""http://www.w3.org/1998/Math/MathML\""><mi>If</mi></math>"",""contentLaTeX"":""$\\mathrm{If}$"",""code"":""KeyI"",""value"":""I""}"
# Math Keypress,1/3/2019 03:31:59.223 PM,"{""numericIdentifier"":""1"",""partId"":"""",""contentMathML"":""<math xmlns=\""http://www.w3.org/1998/Math/MathML\""><mi>If</mi></math>"",""contentLaTeX"":""$\\mathrm{If}$"",""code"":""KeyF"",""value"":""f""}"
# Math Keypress,1/3/2019 03:31:59.792 PM,"{""numericIdentifier"":""1"",""partId"":"""",""contentMathML"":""<math xmlns=\""http://www.w3.org/1998/Math/MathML\""><mi>If</mi><mo>&#xA0;</mo></math>"",""contentLaTeX"":""$\\mathrm{If}\\ $"",""code"":""Space"",""value"":"" ""}"
# Lose Focus,1/3/2019 03:32:02.921 PM,1
# Open Equation Editor,1/3/2019 03:32:02.927 PM,
# Receive Focus,1/3/2019 03:32:08.729 PM,1
# Equation Editor Button,1/3/2019 03:32:09.247 PM,"{""numericIdentifier"":""1"",""partId"":"""",""contentMathML"":""<math xmlns=\""http://www.w3.org/1998/Math/MathML\""><mi>If</mi><mo>&#xA0;</mo><mo>&#x2220;</mo><mfenced open=\""\"" close=\""\""><mrow/></mfenced></math>"",""contentLaTeX"":""$\\mathrm{If}\\ \\angle $"",""what"":""angle""}"
# Math Keypress,1/3/2019 03:32:13.408 PM,"{""numericIdentifier"":""1"",""partId"":"""",""contentMathML"":""<math xmlns=\""http://www.w3.org/1998/Math/MathML\""><mi>If</mi><mo>&#xA0;</mo><mo>&#x2220;</mo><mfenced open=\""\"" close=\""\""><mn>2</mn></mfenced></math>"",""contentLaTeX"":""$\\mathrm{If}\\ \\angle 2$"",""code"":""Digit2"",""value"":""2""}"
# Math Keypress,1/3/2019 03:32:16.472 PM,"{""numericIdentifier"":""1"",""partId"":"""",""contentMathML"":""<math xmlns=\""http://www.w3.org/1998/Math/MathML\""><mi>If</mi><mo>&#xA0;</mo><mo>&#x2220;</mo><mfenced open=\""\"" close=\""\""><mn>2</mn></mfenced><mi>a</mi></math>"",""contentLaTeX"":""$\\mathrm{If}\\ \\angle 2a$"",""code"":""KeyA"",""value"":""a""}"
# Math Keypress,1/3/2019 03:32:17.023 PM,"{""numericIdentifier"":""1"",""partId"":"""",""contentMathML"":""<math xmlns=\""http://www.w3.org/1998/Math/MathML\""><mi>If</mi><mo>&#xA0;</mo><mo>&#x2220;</mo><mfenced open=\""\"" close=\""\""><mn>2</mn></mfenced><mi>and</mi></math>"",""contentLaTeX"":""$\\mathrm{If}\\ \\angle 2\\mathrm{and}$"",""code"":""KeyN"",""value"":""n""}"
# Math Keypress,1/3/2019 03:32:17.383 PM,"{""numericIdentifier"":""1"",""partId"":"""",""contentMathML"":""<math xmlns=\""http://www.w3.org/1998/Math/MathML\""><mi>If</mi><mo>&#xA0;</mo><mo>&#x2220;</mo><mfenced open=\""\"" close=\""\""><mn>2</mn></mfenced><mi>and</mi></math>"",""contentLaTeX"":""$\\mathrm{If}\\ \\angle 2\\mathrm{and}$"",""code"":""KeyD"",""value"":""d""}"
# Math Keypress,1/3/2019 03:32:18.004 PM,"{""numericIdentifier"":""1"",""partId"":"""",""contentMathML"":""<math xmlns=\""http://www.w3.org/1998/Math/MathML\""><mi>If</mi><mo>&#xA0;</mo><mo>&#x2220;</mo><mfenced open=\""\"" close=\""\""><mn>2</mn></mfenced><mi>and</mi><mo>&#xA0;</mo></math>"",""contentLaTeX"":""$\\mathrm{If}\\ \\angle 2\\mathrm{and}\\ $"",""code"":""Space"",""value"":"" ""}"
# Lose Focus,1/3/2019 03:32:19.740 PM,1


def parseMathKeypressEvents(eInfo):
    """Parse the mathematics "Math Keypress" events.

    The 2019 equation editor button events contain the following payload in the ExtendedInfo field:
    # Math Keypress,1/3/2019 03:31:58.978 PM,
    #    "{'numericIdentifier':'1','partId':'',
    #      'contentMathML':'<math xmlns=\'http://www.w3.org/1998/Math/MathML\'><mi>If</mi></math>',
    #      'contentLaTeX':'$\\mathrm{If}$',
    #      'code':'KeyI',
    #      'value':'I'}"
    Note that we renamed the field 'code' as 'mathKeyName'

    :param eInfo: a Pandas series containing ExtendedInfo for "Equation Editor Button" events
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """

    assert (isinstance(eInfo, pd.Series))
    try:
        eInfo = eInfo.str.replace('"code"', '"mathKeyName')
        res = eInfo.apply(parseJsonDatum)
    except:
        #        print "\nWarning: parseMediaEvents: some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res


def parseEquationEditorButtonEvents(eInfo):
    """Parse the mathematics "Equation Editor Button" events.
    
    The 2019 equation editor button events contain the following payload in the ExtendedInfo field:
    # Equation Editor Button,1/3/2019 03:32:09.247 PM,\
    #  "{'numericIdentifier':'1','partId':'',
    #    'contentMathML':'<math xmlns=\'http://www.w3.org/1998/Math/MathML\'><mi>If</mi><mo>&#xA0;</mo><mo>&#x2220;</mo>
    #        <mfenced open=\'\' close=\'\'><mrow/></mfenced></math>',
    #    'contentLaTeX':'$\\mathrm{If}\\ \\angle $',
    #    'what':'angle'}"
    Note that we renamed the field 'what' as 'equationEditorButtonName'

    :param eInfo: a Pandas series containing ExtendedInfo for "Equation Editor Button" events
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """

    assert (isinstance(eInfo, pd.Series))
    try:
        eInfo = eInfo.str.replace('"what"', '"equationEditorButtonName')
        res = eInfo.apply(parseJsonDatum)
    except:
        #        print "\nWarning: parseMediaEvents: some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res



def parseEquationEditorEvents(eInfo):
    """ Placeholder parser for equation events. Depreciated"""
    assert (isinstance(eInfo, pd.Series))
    try:
        res = eInfo.apply(lambda x: {"EquationEditorEvent": x})
    except:
        #        print "\nWarning: parseEquationEditorEvents: some rows of ExtendedInfo cannot be parsed"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res
