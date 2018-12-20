import pandas as pd

from pdia import dropStudents


def dropStudentsWithMultipleZeroTimes(dfStateTime,
                                      stime="stime",
                                      studentId="BookletNumber",
                                      blockId="BlockCode",
                                      saveDroppedAs=None,
                                      verbose=True):
    """
    Dropping students who have multiple zero tile per block.
    
    Normally when we calculate `durSinceBlockStarts`, each block should have a single 0, which should be the first
    row of the block. However, under rare cases (e.g., ???) a block may contain multiple zeros in durSinceTimeStart.
    We drop students who have at least 1 block with this situation; note it's not the offending blocks, it's the student
    being dropped. 
    
    :param dfStateTime: a state-time data frame with data from multiple students
    :param stime: column name of the starting time; default to 'stime'
    :param studentId: name of the column containing the student ID info; default to "BookletNumber"
    :param blockId: naem of the column containing the ID of the block; default to "BlockCode"
    :param saveDroppedAs: optionally saving the dropped data to a csv or pickle file. Remember to specify .csv or .pickle
    :param verbose: default to True
    :return: a data frame with students with multipel zero times dropped.
    """
    # error checks
    # make sure the columns are valid
    if not all([t in dfStateTime.columns.values for t in [studentId, blockId, stime]]):
        raise ValueError('Some columns in [studentId, blockId, stime] are not in the dataframe')

    assert (isinstance(dfStateTime, pd.DataFrame))
    for v in [studentId, blockId, stime]:
        assert (v in dfStateTime.columns)

    counts = dfStateTime.groupby([studentId, blockId]).apply(lambda df: df.loc[df[stime] == 0.0, :].shape[0])

    if verbose:
        print("\ndropStudentsWithMultipleZeroTimes:")
        print("Frequency of zero-time cases per student per block.")
        print("Dropping students with frequency >1.")
    print(counts.value_counts())

    studentsToDrop = counts[counts > 1].reset_index()[studentId].unique()

    return dropStudents(dfStateTime, studentsToDrop,
                        saveDroppedAs=saveDroppedAs,
                        studentId=studentId,
                        verbose=True)
