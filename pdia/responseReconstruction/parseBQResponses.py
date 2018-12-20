
# coding: utf-8

# # Reconstructing 2017 SQ Responses
# 
# ```
# Gary Feng
# 2017-07-14
# ```
# 

import sys

import pandas as pd

from pdia.responseReconstruction.extractBQChoice import parseBQChoice
from pdia.responseReconstruction.extractBQMC import parseBQMC
from pdia.responseReconstruction.extractBQNumeric import parseBQNumeric


def parseStrSQResponses(df,
                     config=None, 
                     label="ItemTypeCode",
                     outputCol = "Answer"):
    """Parse the SQ response data, extract the responses from the JSON data

    :param df: the input data frame
    :type df: Pandas data frame
    
    :param label: optional, name of the column indicating the item type, which determines how to parse.
    :type label: string

    :param config: optional configuation object; default to None
    :type config: object or None

    :returns: df with Response.PartId, Response.Index, value
    :rtype: Pandas data frame

    """

    assert (isinstance(df, pd.DataFrame))
    assert (label in df.columns)

    if config is None:
        config = {
            "handlers": {
                "BQNumeric": parseBQNumeric,
                "BQChoices": parseBQChoice,
                "BQMCSS": parseBQMC,
                "BQMCMS": parseBQMC
            }
        }
    
    # check to see if there are events not handled
    #print config["handlers"]
    #print "Events in the data frame: {}".format(df[label].unique().tolist())
    #print "Events to be handled: {}".format(config["handlers"].keys())
    if len(set(df[label].unique().tolist())-set(config["handlers"].keys()))>0:
        print("Not all item types are handled!\n{}"\
            .format(set(df[label].unique().tolist())-set(config["handlers"].keys())))

    # now let's revert the config, to get `parser:[list of labels]`
    funcMap = {}
    for k, v in config["handlers"].items():
        funcMap[v] = funcMap.get(v, []) + [k]

    # add a output
    # we now loop through all funcMap elements and do the conversion
    for parser, eventList in funcMap.items():
        idx = df.loc[:, label].isin(eventList)
        df.loc[idx, outputCol] = df.loc[idx, "Response"].apply(parser)
    return df


if __name__ == '__main__':

    if len(sys.argv)<2:
        print("Usage: python {} csvFileName.csv".format(sys.argv[0]))
        exit()

    dataFileName = sys.argv[1]

    df = pd.read_csv(dataFileName, sep="\t", header=None,
        names=["ItemResponseId","SubjectName","Grade","BookletNumber",
            "BlockCode","AccessionNumber","ItemTypeCode","IsAnswered",
            "IsSkipped","Response"])

    res = parseStrSQResponses(df)

    # looking for duplicated responses
    res.loc[res.duplicated([ 'BookletNumber', 'AccessionNumber'], keep=False)]\
        .sort_values([ 'BookletNumber', 'AccessionNumber'])\
        .to_csv(dataFileName.replace(".csv", "")+'_DuplicatedResponses.csv')

    dfByAccNum = res.drop_duplicates([ 'BookletNumber', 'AccessionNumber'])\
        .pivot(columns='AccessionNumber', index="BookletNumber", values="Answer")

    # saving to a bunch of csv files
    res.to_csv(dataFileName.replace(".csv", "")+'_Responses.csv')

    dfByAccNum.to_csv(dataFileName.replace(".csv", "")+'_Responses_byAccNum.csv')