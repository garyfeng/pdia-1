import pandas as pd


# This one is taken from stackoverflow
# usage:  df.mask("AccessionNumber", "VH315174")

def mask(df, key, value):
    """
    Filter in only when df[key]==value

    :param df: input data frame
    :param key: name of the column to filter
    :param value: value to keep
    :return: df with filtered value
    """
    assert (isinstance(df, pd.DataFrame))
    assert (key in df.columns)
    return df[df[key] == value]


pd.DataFrame.mask = mask

