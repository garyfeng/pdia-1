import pandas as pd
from pdia import logger
from pdia.responseReconstruction.reconSBTSelectChoice import reconSBTSelectChoice
from pdia.responseReconstruction.reconSBTSelectDrop import reconSBTSelectDrop
from pdia.responseReconstruction.reconSBTText import reconSBTText

try:
    from io import StringIO
except ImportError:
    from io import StringIO


def reconSBTItemResponses(df, config=None):
    """Parse SBT process data, reconstruct responses using an array of functions

    :param df: the input data frame
    :type df: Pandas data frame

    :param config: optional configuation object; default to None
    :type config: object or None

    :returns: df with responses
    :rtype: Pandas data frame

    """

    try:
        assert (isinstance(df, pd.DataFrame))
        assert (config["itemtypeColumn"] in df.columns)
        assert (config["accnumColumn"] in df.columns)
    except Exception as e:
        #logger.error("reconSBTItemResponses: Returning None due to errors")
        #logger.exception(e)
        return None

    # make sure we have relevant events, else return None
    if df.loc[df[config["itemtypeColumn"]].isin(list(config["handlers"].keys()))].shape[0] == 0:
        return None

    if config is None:
        config = {
            "itemtypeColumn": "Label",
            "accnumColumn": "ControlId",
            "outputColumn": "ReconAnswer",
            "handlers": {
                "select.drop": reconSBTSelectDrop,
                "text.blur": reconSBTText,
                "select.choose": reconSBTSelectChoice
            }
        }

    # now let's revert the config, to get `parser:[list of labels]`
    funcMap = {}
    for k, v in config["handlers"].items():
        funcMap[v] = funcMap.get(v, []) + [k]

    # we now loop through all funcMap elements and do the conversion
    # TODO: consider ways to parallelize the process, e.g., using dask
    alldata=[]
    for parser, eventList in funcMap.items():
        idx = df.loc[:, config["itemtypeColumn"]].isin(eventList)
        # alldata.append( df.loc[idx, :].groupby([accnum, itemtype]).apply(parser, accnum=accnum, itemtype=itemtype))
        # alldata.append( df.loc[idx, :].groupby(accnum).apply(parser, accnum=accnum, itemtype=itemtype))
        tmp = df.loc[idx, :]\
            .groupby(config["accnumColumn"])\
            .apply(parser, accnum=config["accnumColumn"], itemtype=config["itemtypeColumn"])
        if tmp.shape[0] > 0:
            alldata.append(tmp)

    # concat data
    try:
        res = pd.concat(alldata).reset_index()
        res.columns = [config["accnumColumn"], config["outputColumn"]]
    except Exception as e:
        logger.error("reconSBTItemResponses: Returning None due to errors")
        logger.exception(e)
        return None
    return res
