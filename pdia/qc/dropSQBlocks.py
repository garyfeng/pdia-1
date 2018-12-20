import pandas as pd

from pdia import dropBlocksMatching


def dropSQBlocks(df, sqBlockKey="QSTX",
                 blockKey="BlockCode",
                 verbose=True):
    """ Drop SQ blocks

    :param df: eNAEP observable data frame
    :param sqBlockKey: regex of the block names to drop
    :param blockKey: the column name in the df indicating the block names
    :param verbose: default to True
    :return: eNAEP observable data frame
    """

    # error checks
    assert (isinstance(df, pd.DataFrame))
    assert (blockKey in df.columns)

    return dropBlocksMatching(df, blockPattern=sqBlockKey, blockKey=blockKey, verbose=verbose)

