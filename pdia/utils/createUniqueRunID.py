import pandas as pd

from pdia.utils.countVisits import countVisits


def createUniqueRunID(df, var='onScreen', runId='onScreenRunID'):
    """Create a new column with countVisits()

    :param df: data frame
    :param var: name of the column from which we are creating the runs
    :param runId: name of the column we will create to hold the unique runs
    :return: the df with the new column of runId
    """

    assert (isinstance(df, pd.DataFrame))
    assert (var in df.columns)

    df.loc[:, runId] = countVisits(df[var])
    return df
