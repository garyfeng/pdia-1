from pdia.extendedInfoParser.parseJSON import parseJsonDatum


def parseMathML(js):
    """Parse a JSON string, return parsed object without the MathML.

    The current observable log for MathML includes both the "contentMathML"
    and an latex field. Here we just want to return the latex. We can simply
    ignore the `contentMathML`.

    In the case one needs to translate MathML expressions to latex, use
    pdia.utils.mml2latex().

    :param js: input JSON string
    :return: parsed dict object without the "contentMathML" part
    """
    res = parseJsonDatum(js)
    # Now get rid of the MathML
    try:
        del res['contentMathML']
    except:
        pass

    return res
