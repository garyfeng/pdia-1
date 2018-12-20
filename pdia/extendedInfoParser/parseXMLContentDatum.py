from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ParseError

from pdia import logger
from pdia.extendedInfoParser.parseJSON import parseJsonDatum

def parseXMLContentDatum(s):
    """Parses a XML <content> element, returns a dict.

    Input: "<content><pair><key>description</key><value>3</value></pair></content>"
    Output: {'description': '3'}

    In the case the content string is a JSON, it returns the parsed JSON.

    :param s string containing the XML, or a XML node
    :return a dict of key-value pairs

    """

    Element = type(ET.Element(None))

    if isinstance(s, str):
        # presum it's a XML string
        try:
            root = ET.fromstring(s)
        except ParseError:
            #logger.warning("parseXMLContentDatum: cannot parse the source string; returning as parsed JSON")
            #logger.warning("    Content: {}".format(s))
            return parseJsonDatum(s)
    elif isinstance(s, Element):
        # xml element
        root = s
    else:
        logger.warning("parseXMLContentDatum: source should be either a XML string or XML node; returning None")
        return None

    r = {}
    for pair in root.iter('pair'):
        key = pair.find('key').text
        value = pair.find('value').text
        r[key] = value
    return r