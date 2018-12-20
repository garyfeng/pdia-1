
# coding: utf-8

import pandas as pd

try:
    from io import StringIO
except ImportError:
    from io import StringIO

# be explicit for what to import
# from pdia import *
from pdia.responseReconstruction.extractBQChoice import parseBQChoice
from pdia.responseReconstruction.extractBQNumeric import parseBQNumeric
from pdia.responseReconstruction.extractBlockReview import parseBlockReview
from pdia.responseReconstruction.extractComposite import parseComposite
from pdia.responseReconstruction.extractDialog import parseDialog
from pdia.responseReconstruction.extractExtendedText import parseExtendedText
from pdia.responseReconstruction.extractFillInBlank import parseFillInBlank
from pdia.responseReconstruction.extractGridMS import parseGridMS
from pdia.responseReconstruction.extractIIC import parseInteractive
from pdia.responseReconstruction.extractInlineChoiceListMS import parseInlineChoiceListMS
from pdia.responseReconstruction.extractMC import extractMC
from pdia.responseReconstruction.extractMatchMS import parseMatchMS
from pdia.responseReconstruction.extractSBT import extractSBT
from pdia.responseReconstruction.extractBQNotAnswered import extractBQNotAnswered
from pdia.responseReconstruction.extractZone import parseZones


# json can't load unicode strings.
# had to use ast: https://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-from-json

def parseItemResponses(df,
                       config=None):
    """Parse the SQ response data, extract the responses from the JSON data

    :param df: the input data frame
    :type df: Pandas data frame

    :param config: optional configuation object; default to None
    :type config: object or None

    :returns: df with Response.PartId, Response.Index, value
    :rtype: Pandas data frame

    """

    if config is None:
        config = {
            "itemtypeColumn":"ItemTypeCode",
            "responseColumn":"Response",
            "outputCol":"Answer",
            "handlers": {
                "BQNumeric": parseBQNumeric,
                "BQChoices": parseBQChoice,
                "BQMCSS": extractMC,
                "BQMCMS": extractMC,
                "ZonesMS": parseZones,
                "ZonesSS": parseZones,
                "GridMS": parseGridMS,
                "ReadingNonSBT": extractSBT,
                "SBT": extractSBT,
                "ExtendedText": parseExtendedText,
                "InlineChoiceListMS": parseInlineChoiceListMS,
                "Interactive": parseInteractive,
                "Composite": parseComposite,
                "CompositeCR": parseComposite,
                "FillInBlank": parseFillInBlank,
                "MultipleFillInBlank": parseFillInBlank,
                "SQNotAnswered": extractBQNotAnswered,
                "MCMS": extractMC,
                "MCSS": extractMC,
                "MatchMS ": parseMatchMS,
                "Dialog": parseDialog,
                "Directions": parseDialog,
                "BlockReview": parseBlockReview,
                "TimeLeftMessage": parseDialog,
                "TimeOutMessage": parseDialog,
                "ThankYou": extractMC
            }
        }

    assert (isinstance(df, pd.DataFrame))
    assert (config["itemtypeColumn"] in df.columns)
    assert (config["responseColumn"] in df.columns)

    # now let's revert the config, to get `parser:[list of labels]`
    funcMap = {}
    for k, v in config["handlers"].items():
        funcMap[v] = funcMap.get(v, []) + [k]

    # we now loop through all funcMap elements and do the conversion
    # TODO: consider ways to parallelize the process, e.g., using dask
    for parser, eventList in funcMap.items():
        idx = df.loc[:, config["itemtypeColumn"]].isin(eventList)
        df.loc[idx, config["outputCol"]] = df.loc[idx, config["responseColumn"]].apply(parser)
    return df


