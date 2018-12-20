def getVal(json, key):
    """
    given a dict object and a key, return the value associated with key; returns None if the
    key does not exist in the JSON object.

    This is the fastest method for accessing the value of a JSON given a key, but least flexible.
    It does not handle hierarchical JSON paths.

    :param json: a dict object
    :param key: the key (cann't handle a json path)
    :return: the value associated with the key, or None
    """
    # make sure this is JSON
    # parse('textDiff.diffs.[*].len').find(j)[0].value

    try:
        res = json[key]
    except:
        res = None
    return res