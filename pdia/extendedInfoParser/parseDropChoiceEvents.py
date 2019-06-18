from pdia.extendedInfoParser.parseExtendedInfo import errorCode
from pdia.extendedInfoParser.parseJSON import parseJsonDatum
from pdia.extendedInfoParser.parseXMLContentDatum import parseXMLContentDatum

def parseDropChoice(eInfo):
    """parse DropChoice event, xml content

    The ExtendedInfo typically contains a JSON string like

    '[{"source":"2","target":"1"},{"source":"7","target":"2"}]'

    or in some cases an XML string 

    We return a JSON/dict and wrap the result like

    {"DropChoiceResponse": [{"source":"2","target":"1"},{"source":"7","target":"2"}]}

    :param eInfo: a Pandas series containing ExtendedInfo events
    :return: a parsed series of JSON/DICT objects, or errorCode if error    
    """

    assert (isinstance(eInfo, object))
    try:
        res = eInfo.apply(lambda x: {"DropChoiceResponse":parseJsonDatum(x, flatten=False)} )
    except:
        try:
            res = eInfo.apply(lambda x: {"DropChoiceResponse":parseXMLContentDatum(x)})
        except:
            return(eInfo.apply(errorCode))
    return res