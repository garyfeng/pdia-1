import pandas as pd


def dropDuplicatedResponses(dfResponses, dupIdColumns=None, returnDups=False):
    """
    Take a parsed response data frame, returns a data frame after dropping duplications

    :param dfResponses: data frame with responses
    :param dupIdColumns: a list of column names to keep track when we identify duplications.
    :param returnDups: optionally return duplicated records instead of non-duplicated; default to False
    :return: df with duplications eliminated, unless returnDups == True, in which case return only dups
    """
    assert (isinstance(dfResponses, pd.DataFrame))
    if dupIdColumns is None:
        dupIdColumns = ['BookletNumber', 'AccessionNumber']
    assert (label in dfResponses.columns for label in dupIdColumns)

    # looking for duplicated responses
    if returnDups:
        return dfResponses.loc[dfResponses.duplicated(dupIdColumns, keep=False)].sort_values(dupIdColumns)
    else:
        return dfResponses.drop_duplicates(dupIdColumns)
