import pandas as pd

from pdia import dropStudents


def dropStudentsWithEvents(df, events,
                           saveDroppedAs=None,
                           studentId='BookletNumber',
                           eventId='Label',
                           verbose=True):
    """
    Drop students with certain events.

    It finds students with the events, and use dropStudents() to drop them.

    :param df: input data frame with data from multiple students
    :param events: a list of events. Each event is a string of event name
    :param saveDroppedAs: optionally saving the dropped data to a csv or pickle file. Remember to specify .csv or .pickle
    :param studentId: name of the column containing the student ID info; default ot "BookletNumber"
    :param eventId: name of the column containing the event name; default to "Label"
    :param verbose: default to True
    :return: a data frame with students having any of these events dropped.
    """

    # error checks
    assert (isinstance(df, pd.DataFrame))
    for v in [studentId, eventId]:
        assert (v in df.columns)

    studentsToDrop = df.loc[df[eventId].isin(events), studentId].unique()
    if verbose:
        print("\ndropStudentsWithEvents:")
        print(events)

    return dropStudents(df, studentsToDrop, saveDroppedAs, studentId, verbose)
