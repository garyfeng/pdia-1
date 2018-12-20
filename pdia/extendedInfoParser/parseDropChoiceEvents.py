from pdia.extendedInfoParser.parseJSON import parseJsonDatum
from pdia.extendedInfoParser.parseXMLContentDatum import parseXMLContentDatum

def parseDropChoice(eInfo):
    """parse DropChoice event, xml content
    """

    assert (isinstance(eInfo, object))
    try:
        res = eInfo.apply(parseXMLContentDatum)
    except:
        res = eInfo.apply(parseJsonDatum)
    return res