import pandas as pd

from pdia.utils.createUniqueRunID import createUniqueRunID
from pdia.qc.dropStudents import dropStudents


def dropStudentsWithRepeatedBlock(df,
                                  saveDroppedAs=None,
                                  studentId='BookletNumber',
                                  blockId="BlockCode",
                                  runId="blockRunID",
                                  verbose=True):
    """
    Drop students with repeated blocks.

    We keep track of whether the same blocks have been run multiple times. This could happen when, for example,
    a student started a block, got interrupted, and did another block, and asked by the admin to go back to a block.

    But more likely, some intervening "blockID" get inserted into a contiguous blockID, creating the illusion of
    a block being run multiple times. The latter case is often salvageable.

    So when possible, investigate such cases and come up with a fix.

    :param df: input data frame with data from multiple students
    :param saveDroppedAs: optionally saving the dropped data to a csv or pickle file. Remember to specify .csv or .pickle
    :param studentId: name of the column containing the student ID info; default ot "BookletNumber"
    :param runId: name of the column containing the run counter of blocknames; default to "blockRunID"
    :param verbose: default to True
    :return: a data frame with students having any of these events dropped.

    """

    # error checks
    assert (isinstance(df, pd.DataFrame))
    for v in [studentId, blockId]:
        assert (v in df.columns)

    if verbose:
        print("\ndropStudentsWithRepeatedBlock:")

    # compute the blockRunID, and keep only the first line per Student by blockRunID
    t2 = df.groupby([studentId]) \
        .apply(lambda x: createUniqueRunID(x, var=blockId, runId=runId)) \
        .groupby([studentId, runId]).first() \
        .reset_index()
    # find the # of unique BlockCode != the total number of block runs
    idx = t2.groupby([studentId])[blockId].nunique() < t2.groupby([studentId])[runId].max()
    # find the studentID: make sure it's a Pandas Series
    studentsToDrop = pd.Series(idx[idx == True].index)

    if verbose:
        print("dropStudentsWithRepeatedBlock:")

    return dropStudents(df, studentsToDrop, saveDroppedAs, studentId, verbose)
