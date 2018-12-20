import pandas as pd

# now before we reset_index() to "ungroup", we need to remove the "BookletNumber" and "BlockCode" blocks
#  from the df, because we have used reset_index() in some of the pipe code, which would have created these
#  columns in the df. It's from the `addKeyPressVars()` function where I used join(), probably.
# ~~So we need to use .reset_index(drop=True)~~ But we cannot.
# workaround: since I can't drop the columns, I use the old set trick:

def resetIndexDropDup(df, groupVars, indexColumn="ObservableEventId"):
    """
    Reset index of a data frame to the "defaultIndex" while taking care
     of duplicated groupVars columns

    :param df: data frame with potential duplicated groupVars columns
    :param groupVars: a list of column names that are potentially duplicated
    :param indexColumn: the name of the column that is intended as the index
    :return: data frame with the defaultIndex as the index

    Examples:

        # will do later. Just setting up the config
        groupVars = ["BookletNumber", "AccessionNumber", "BlockCode"]
        defaultIndex = df.index.name

        df = df\
            .groupby(groupVars)\
            .apply(testIt)\
            .pipe(resetIndexDropDup, groupVars = groupVars, defaultIndex = defaultIndex)
    """
    assert (isinstance(df, pd.DataFrame))
    assert (indexColumn in df.columns)
    assert (all([v in df.columns for v in groupVars]))

    clist = list(set(df.columns) - set(groupVars))
    df = df[clist].reset_index().set_index(indexColumn)
    return df