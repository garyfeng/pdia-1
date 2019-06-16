import ast
import json
import pandas as pd
from pdia.utils.flatten_dict import flatten_dict

def parseJsonDatum(js, flatten=True):
    """Parse a JSON string, return parsed object or None.

    We will flatten the dict as an option. By flatten we mean the following:
    a hierarchical json like {"a":1, "b":{"c":2, "d":3}} will become
    {"a":1, "b.c":2, "b.d":3}, where "." is an optional separator parameter
    defaulting to ".".

    :rtype:
    :param js: A valid JSON string
    :param flatten: Option to return a flattened json; default to True
    :return parsed JSON as a dict; None if js is not a string; js if it is a
        string but not a valid json string
    """

    if isinstance(js, dict):
        return js

    try:
        basestring
    except NameError:
        basestring = str

    if not isinstance(js, basestring):
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

    # let's see if we flatten the json output
    if flatten:
        res = flatten_dict(res)
    return res


