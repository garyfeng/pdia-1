import pandas as pd


def dropBlocksMatching(df, blockPattern,
                 blockKey="BlockCode",
                 verbose=True):
    """ Drop blocks that match a regular expression

    :param df: eNAEP observable data frame
    :param blockPattern: regex of the block names to drop
    :param blockKey: the column name in the df indicating the block names
    :param verbose: default to True
    :return: eNAEP observable data frame
    """

    # error checks
    assert (isinstance(df, pd.DataFrame))
    assert (blockKey in df.columns)

    sizeBeforeDropping = df.shape[0]
    idx = df[blockKey].str.contains(blockPattern)
    df = df[~ idx]
    if verbose:
        print("\nDrop blocks matching " + blockPattern)
        print("Total number of evens before = %s" % (sizeBeforeDropping))
        print("Total number of evens after  = %s" % (df.shape[0]))
    return df


