import pandas as pd
try:
    from io import StringIO
except ImportError:
    from io import StringIO

from pdia.responseReconstruction.reconMC import reconMCSS, reconMCMS


def reconItemResponses(df, config=None):
    """Parse process data, reconstruct responses using an array of functions.

    This returns a data frame with only rows containing reconstructed responses. In other words:
    - if the item is not handled by one of the config[handlers], then no output for that item
    - if there are log entries for an item type that is handled, but the log does not contain any actions that change the
    state of the responses (e.g., the student made no attempt to touch any of the items in this item type), then the
    reconstruction returns nothing, and the data for this item type will be excluded from output.
    - if an item type is handled, and some of the items had no actions to reconstruct, the item responses will be None

    :param df: the input data frame
    :type df: Pandas data frame

    :param config: optional configuation object; default to None
    :type config: object or None

    :returns: df with responses
    :rtype: Pandas data frame

    """

    if config is None:
        config = {
            "itemtypeColumn": "ItemTypeCode",
            "accnumColumn": "AccessionNumber",
            "outputColumn": "ReconAnswer",
            "extInfoColumn": "extInfo",
            "maxNumberOfOptions": 10,
            "handlers": {
                "BQMCSS": reconMCSS,
                "BQMCMS": reconMCMS,
                "MCSS": reconMCSS,
                "MCMS": reconMCMS
            }
        }

    assert (isinstance(df, pd.DataFrame))
    assert (config["itemtypeColumn"] in df.columns)
    assert (config["accnumColumn"] in df.columns)

    # now let's revert the config, to get `parser:[list of labels]`
    funcMap = {}
    for k, v in config["handlers"].items():
        funcMap[v] = funcMap.get(v, []) + [k]

    # we now loop through all funcMap elements and do the conversion
    # TODO: consider ways to parallelize the process, e.g., using dask
    alldata=[]
    for parser, eventList in funcMap.items():
        idx = df.loc[:, config["itemtypeColumn"]].isin(eventList)
        # alldata.append( df.loc[idx, :].groupby(config["accnumColumn"]).apply(parser))
        # don't add df if no answer can be constructed, i.e., if the student made no attempt to
        # change the state of any item in this item type.
        tmp = df.loc[idx, :].groupby(config["accnumColumn"]).apply(parser, config=config)
        if tmp.shape[0] > 0:
            alldata.append(tmp)

    # concat data
    try:
        res = pd.concat(alldata)
    except:
        res = None
    return res



