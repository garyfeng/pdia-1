import pandas as pd

from pdia.utils.createUniqueRunID import createUniqueRunID


def dropSupplementalBlocks(df, requiredBlockNumber=2,
                           studentId='BookletNumber',
                           blockId="BlockCode",
                           runId="blockRunID",
                           verbose=True):
    """Dropping supplemental blocks, which some students may take after completing the
   required 2 blocks. Note:
   - should first drop students with multiple runs of the same blocks
   - this also get rid of SQ blocks, in principle.

    :param studentId:
    :param blockId:
    :param runId:
    :param verbose:
   :param df: the dataframe containing process data
   :type df: Pandas data frame

   :param requiredBlockNumber: the number of required blocks before supplemental blocks start
   :type requiredBlockNumber: int

   :returns df after dropping supplemental blocks
   :rtype Pandas data frame

    """

    # error checks
    assert (isinstance(df, pd.DataFrame))
    for v in [studentId, blockId]:
        assert (v in df.columns)

    sizeBeforeDropping = df.shape[0]
    if verbose:
        print("\ndropSupplementalBlocks:")
        print("\nDrop supplimental blocks (>" + str(requiredBlockNumber) + ")")
        print("Total number of evens before = %s" % (sizeBeforeDropping))

    # compute the blockRunID
    df = df.groupby([studentId]).apply(lambda x: createUniqueRunID(x, var=blockId, runId=runId))

    # keeping only non-supplimental blocks, where runId is 1-based.
    df = df.loc[df[runId] <= requiredBlockNumber, :]
    if verbose:
        print("Total number of evens after  = %s" % (df.shape[0]))
    return df
