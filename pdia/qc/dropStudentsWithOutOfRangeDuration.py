import pandas as pd

from pdia import dropStudents


def dropStudentsWithOutOfRangeDuration(dfStateTime,
                                       minDur=0, maxDur=20 * 60,  # in seconds
                                       dur="dur",
                                       studentId="BookletNumber",
                                       blockId="BlockCode",
                                       stateValueColumn="value",
                                       stateValues=None,
                                       saveDroppedAs=None,
                                       verbose=True):
    """
    Drop students with any event with duration outside of the range [minDur, maxDur].

    if stateValues is specified (either as a list of a string), then we only filter the dur by these events.

    :param dfStateTime: a state-time data frame with data from multiple students
    :param dur: column name of the duration; default to 'dur'
    :param minDur: the minimal duration of an event; default to 0
    :param maxDur: the max duration of an event; default to 20 minutes, or 1,200 seconds
    :param stateValueColumn: name of the column for "state Values"
    :param stateValues: the state value (as a string) or values (as a list of strings) to filter; if None, all events are used in the filter
    :param studentId: name of the column containing the student ID info; default to "BookletNumber"
    :param blockId: naem of the column containing the ID of the block; default to "BlockCode"
    :param saveDroppedAs: optionally saving the dropped data to a csv or pickle file. Remember to specify .csv or .pickle
    :param verbose: default to True
    :return: a data frame with students with multipel zero times dropped.
    """

    # error checks
    assert (isinstance(dfStateTime, pd.DataFrame))
    for v in [studentId, blockId, dur]:
        assert (v in dfStateTime.columns)

    if verbose:
        print("\ndropStudentsWithOutOfRangeDuration:")
        print("Limiting " + dur + " to [" + str(minDur) + ", " + str(maxDur) + "].")

    if stateValues is None:
        counts = dfStateTime.groupby([studentId, blockId]).apply(
            lambda df: df.loc[(df[dur] < minDur) & (df[dur] > maxDur), :].shape[0])
    else:
        if stateValueColumn not in dfStateTime.columns.values:
            raise ValueError('"' + stateValueColumn + '" is not in the dataframe')
        # make sure stateValue is a list-like
        if isinstance(stateValues, str):
            stateValues = [stateValues]
        if verbose:
            print("Limiting " + stateValueColumn + " to " + str(stateValues) + ".")

        counts = dfStateTime \
            .groupby([studentId, blockId]) \
            .apply(lambda df: df.loc[((df[dur] < minDur) | (df[dur] > maxDur))
                                     & df[stateValueColumn].isin(stateValues), :].shape[0])

    if verbose:
        print("Frequency of out-of-range cases per student per block")
        print(counts.value_counts())

    studentsToDrop = counts[counts > 0].reset_index()[studentId].unique()

    return dropStudents(dfStateTime, studentsToDrop,
                        saveDroppedAs=saveDroppedAs,
                        studentId=studentId,
                        verbose=True)
