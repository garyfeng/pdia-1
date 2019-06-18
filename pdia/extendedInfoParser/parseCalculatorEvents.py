import pandas as pd
from pdia.extendedInfoParser.parseJSON import parseJsonDatum
from pdia.extendedInfoParser.parseExtendedInfo import errorCode

# Open Calculator,1/3/2019 03:08:12.621 PM,TI30
# Move Calculator,1/3/2019 03:08:15.763 PM,TI30
# Calculator Keystroke Logging,1/3/2019 03:08:18.214 PM,"{""model"":""TI30"",""key"":""TI30XS_KEY_4_NONE"",""val"":""0"",""screen"":""data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMAAAABLCAYAAAAmq4gcAAACmklEQVR4Xu3a0U6DUBRE0fL/H11TE0yDrSjN5Ix0+WJs5dxhD9ur4HK9Xq8XHwi8SGBZls8J6+W0fr332ovLvnz4QoCXGRpwuVxuF/zt4t9+XuGsr7fBIkBbI/80zyMB1lPZinG/K0yfLgGmGzjJ+n/ZAZp2AwKc5AKcPg1/A0w3YH0EDhCwAxyA5pDzECDAebp0JgcI7Aqw/d3u/rbWb9bzmOE3lHzPFAECTJG3bgWBpwLcP8l7dN92+/6zs7EDVPQsxBMCBHBpvDWBbwI8u5+7/UluB3jr6+Y0J0+A01TpRI4Q+BJg726PHeAIXse0EyBAe0PyRQl8E2BvtUf/7/3TMe4C7RH1/iQBAkzSt/Y4AQ/CxisQYJIAASbpW3ucAAHGKxBgkgABJulbe5zArgDjCQVAIEiAAEG4RvcTIEB/RxIGCRAgCNfofgIE6O9IwiABAgThGt1PgAD9HUkYJECAIFyj+wkQoL8jCYMECBCEa3Q/AQL0dyRhkAABgnCN7idAgP6OJAwSIEAQrtH9BAjQ35GEQQIECMI1up8AAfo7kjBIgABBuEb3EyBAf0cSBgkQIAjX6H4CBOjvSMIgAQIE4RrdT4AA/R1JGCRAgCBco/sJEKC/IwmDBAgQhGt0PwEC9HckYZAAAYJwje4nQID+jiQMEiBAEK7R/QQI0N+RhEECBAjCNbqfAAH6O5IwSIAAQbhG9xMgQH9HEgYJECAI1+h+AgTo70jCIAECBOEa3U+AAP0dSRgkQIAgXKP7CRCgvyMJgwQIEIRrdD8BAvR3JGGQAAGCcI3uJ0CA/o4kDBIgQBCu0f0ECNDfkYRBAgQIwjW6nwAB+juSMEiAAEG4RvcTIEB/RxIGCRAgCNfofgIE6O9IwiCBD5Tjxy/n+3xwAAAAAElFTkSuQmCC""}"
# ...
# Close Calculator,1/3/2019 03:10:05.090 PM,TI30
# Calculator Buffer,1/3/2019 03:10:05.096 PM,"[""TI30XS_KEY_4_NONE"",""TI30XS_KEY_DIVIDE_K"",""TI30XS_KEY_3_NONE"",""TI30XS_KEY_ENTER_NONE"",""TI30XS_KEY_MULTIPLY_NONE"",""TI30XS_KEY_5_NONE"",""TI30XS_KEY_X2_SQRT"",""TI30XS_KEY_ENTER_NONE"",""TI30XS_KEY_CLEAR_NONE"",""TI30XS_KEY_5_NONE"",""TI30XS_KEY_0_RESET"",""TI30XS_KEY_0_RESET"",""TI30XS_KEY_DIVIDE_K"",""TI30XS_KEY_3_NONE"",""TI30XS_KEY_ENTER_NONE"",""TI30XS_KEY_CLEAR_NONE"",""TI30XS_KEY_4_NONE"",""TI30XS_KEY_DIVIDE_K"",""TI30XS_KEY_3_NONE"",""TI30XS_KEY_ENTER_NONE"",""TI30XS_KEY_MULTIPLY_NONE"",""TI30XS_KEY_5_NONE"",""TI30XS_KEY_X2_SQRT"",""TI30XS_KEY_DELETE_INSERT"",""TI30XS_KEY_3_NONE"",""TI30XS_KEY_DELETE_INSERT"",""TI30XS_KEY_CARET_XSQRT"",""TI30XS_KEY_3_NONE"",""TI30XS_KEY_ENTER_NONE"",""TI30XS_KEY_2ND_NONE"",""TI30XS_KEY_TABLE_FTOD"",""TI30XS_KEY_ENTER_NONE""]"

def parseCalculatorEvents(eInfo):
    """Parse a calculator event string, return parsed object or errorCode.

    This function handles the "Open Calculator", "Move Calculator", and "Close Calculator" events in 2019. Sample
    data:

    # Open Calculator,1/3/2019 03:08:12.621 PM,TI30
    # Move Calculator,1/3/2019 03:08:15.763 PM,TI30
    # Close Calculator,1/3/2019 03:10:05.090 PM,TI30

    :param eInfo: a Pandas series containing ExtendedInfo
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """
    assert (isinstance(eInfo, pd.Series))
    try:
        res = eInfo.apply(lambda x: {"CalculatorModel": x})
    except:
        #        print "\nWarning: parseCalculatorEvents(): some rows of ExtendedInfo is not a string"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res


def parseCalculatorKeystrokeLoggingEvents(eInfo):
    """Parse a calculator event string, return parsed object or errorCode.

    This function handles the "Calculator Keystroke Logging" events in 2019. Sample data:

    # Calculator Keystroke Logging,1/3/2019 03:08:18.214 PM,\
    # "{""model"":""TI30"",
    # ""key"":""TI30XS_KEY_4_NONE"",
    # ""val"":""0"",\
    # ""screen"":""data:image/png;base64,iVBORw0KGgoAAAANSUhEU...""}"
    Note we change the name of the json keys to indicate calculator events.

    :param eInfo: a Pandas series containing ExtendedInfo
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """
    assert (isinstance(eInfo, pd.Series))
    try:
        eInfo = eInfo.str.replace('"model"', '"CalculatorModel"') \
                     .str.replace('"key"', '"CalculatorKey"')\
                     .str.replace('"val"', '"CalculatorCPUValue"')
        res = eInfo.apply(parseJsonDatum)
    except:
        #        print "\nWarning: parseCalculatorEvents(): some rows of ExtendedInfo is not a string"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res


def parseCalculatorBuffer(eInfo):
    """Parse a calculator buffer string, return parsed object or errorCode.

    This function handles the "Calculator Buffer" events in 2019. The content is a list of calculator
    key names between the Open and Close events. Sample data:

    # Calculator Buffer,1/3/2019 03:10:05.096 PM,"[""TI30XS_KEY_4_NONE"",""TI30XS_KEY_DIVIDE_K"",""TI30XS_KEY_3_NONE"",
    #  ""TI30XS_KEY_ENTER_NONE"",""TI30XS_KEY_MULTIPLY_NONE"",""TI30XS_KEY_5_NONE"",""TI30XS_KEY_X2_SQRT"",
    #  ""TI30XS_KEY_ENTER_NONE"",""TI30XS_KEY_CLEAR_NONE"",""TI30XS_KEY_5_NONE"",""TI30XS_KEY_0_RESET"",
    # ""TI30XS_KEY_0_RESET"",""TI30XS_KEY_DIVIDE_K"",""TI30XS_KEY_3_NONE"",""TI30XS_KEY_ENTER_NONE"",
    # ""TI30XS_KEY_CLEAR_NONE"",""TI30XS_KEY_4_NONE"",""TI30XS_KEY_DIVIDE_K"",""TI30XS_KEY_3_NONE"",
    # ""TI30XS_KEY_ENTER_NONE"",""TI30XS_KEY_MULTIPLY_NONE"",""TI30XS_KEY_5_NONE"",""TI30XS_KEY_X2_SQRT"",
    # ""TI30XS_KEY_DELETE_INSERT"",""TI30XS_KEY_3_NONE"",""TI30XS_KEY_DELETE_INSERT"",""TI30XS_KEY_CARET_XSQRT"",
    # ""TI30XS_KEY_3_NONE"",""TI30XS_KEY_ENTER_NONE"",""TI30XS_KEY_2ND_NONE"",""TI30XS_KEY_TABLE_FTOD"",
    # ""TI30XS_KEY_ENTER_NONE""]"

    :param eInfo: a Pandas series containing ExtendedInfo
    :return: a parsed series of JSON/DICT objects, or errorCode if error
    """
    assert (isinstance(eInfo, pd.Series))
    try:
        res = eInfo.apply(lambda x: {"CalculatorBuffer": x})
    except:
        #        print "\nWarning: parseCalculatorBuffer(): some rows of ExtendedInfo is not a string"
        #        return parseDefault(eInfo)
        res = eInfo.apply(lambda x: errorCode)
    return res