import dpath.util


def getVal_dpath(json, key):
    """
    Using dpath: given a JSON object and a key, return the value associated with key; returns None if the
    key does not exist in the JSON object.

    This is 1000x slower than getVal using dict

    :param json: a JSON object or a dict object
    :param key: the key, which can be a dpath
    :return: the value associated with the key, or None
    """
    # make sure this is JSON
    # parse('textDiff.diffs.[*].len').find(j)[0].value
    try:
        res = dpath.util.get(json, key)
    except:
        res = None
    return res