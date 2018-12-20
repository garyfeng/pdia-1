def flatten_dict(dd, separator='_', prefix=''):
    """
    Flattens a dict iteratively and returns a set

    credit: http://stackoverflow.com/questions/6027558/flatten-nested-python-dictionaries-compressing-keys

    :param dd: the input dict
    :param separator: separater character for combining hierarchical keys
    :param prefix: prefix character
    :return: a set with flattened values

    :Example:

    >>>> flatten_dict({'abc':123, 'hgf':{'gh':432, 'yu':433}, 'gfd':902, 'xzxzxz':{"432":{'0b0b0b':231}, "43234":1321}}, '.')
    {'abc': 123,
     'gfd': 902,
     'hgf.gh': 432,
     'hgf.yu': 433,
     'xzxzxz.432.0b0b0b': 231,
     'xzxzxz.43234': 1321}
    """
    return {prefix + separator + k if prefix else k: v
            for kk, vv in list(dd.items())
            for k, v in list(flatten_dict(vv, separator, kk).items())
            } if isinstance(dd, dict) else {prefix: dd}