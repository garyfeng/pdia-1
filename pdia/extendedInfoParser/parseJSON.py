import ast
import json
import pandas as pd


def parseJsonDatum(js):
    """Parse a JSON string, return parsed object or None

    :rtype:
    :param js A valid JSON string
    :return parsed JSON as a dict
    """

    if isinstance(js, dict):
        return js

    if not isinstance(js, str):
        return None

    try:
        # print "JSON: "+js
        res = json.loads(js)
    except:
        try:
            # print "JSON didn't work\n Trying AST"
            res = ast.literal_eval(js)
        except:
            res = js
    return res


