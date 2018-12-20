from pdia.extendedInfoParser.parseJSONObservables import parseJSONObservables


def parseYesNo(eInfo):
    """Parse Yes/No
    Example: {u'Event': u'EOSTimeLeft', u'Language': u' ENG'}
    We will use parseJSON instead.
    """

    return parseJSONObservables(eInfo)