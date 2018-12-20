import pandas as pd

from pdia import dropStudents


def dropStudentsWithMinEvents(df,
                              saveDroppedAs=None,
                              studentId='BookletNumber',
                              blockId="BlockCode",
                              minEvents=3,
                              verbose=True):
    """Drop students with fewer than a certain number events.

    Note that we are dropping students who has at least 1 block having less then minEvents, not just the offending blocks.

    :param df: input data frame with data from multiple students
    :param minEvents: the minimal number of events in each block
    :param saveDroppedAs: optionally saving the dropped data to a csv or pickle file. Remember to specify .csv or .pickle
    :param studentId: name of the column containing the student ID info; default ot "BookletNumber"
    :param blockId: naem of the column containing the ID of the block; default to "BlockCode"
    :param verbose: default to True
    :return: a data frame with students having any of these events dropped.
    """

    # error checks
    assert (isinstance(df, pd.DataFrame))
    for v in [studentId, blockId]:
        assert (v in df.columns)

    # compute the blockRunID, and keep only the first line per Student by blockRunID
    t2 = df.groupby([studentId])[blockId].count().reset_index()
    studentsToDrop = t2.loc[t2[blockId] < minEvents, studentId]

    if verbose:
        print("\ndropStudentsWithMinEvents: minimal events = " + str(minEvents))

    return dropStudents(df, studentsToDrop, saveDroppedAs, studentId, verbose)
