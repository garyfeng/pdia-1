import os
import warnings

import pandas as pd

def dropStudents(df, studentsToDrop,
                 saveDroppedAs=None,
                 studentId='BookletNumber',
                 verbose=True):
    """
    Drop specified students from the data, optionally save the dropped data.

    :param df: a data frame with multiple students
    :param studentsToDrop: a list of the BookletNumber for students to drop
    :param saveDroppedAs: Optionally saving the dropped student data to a filename as CSV or pickle. Specify the file
        extension as either .csv or .pickle
    :param studentId: string; name of the column marking studentId column. Default to "BookletNumber"
    :param verbose: Boolean; default to True
    :return: a pandas data frame, with designated students dropped from the input data frame
    """

    # error checks
    assert (isinstance(df, pd.DataFrame))
    assert (studentId in df.columns)

    if verbose:
        print("\nTotal number of evens in df      = %s" % (df.shape[0]))
        print("Total number of students in df   = %s" % (df[studentId].unique().shape[0]))
        print("Total number of Students to drop = %s" % (studentsToDrop.size))
    sizeBeforeDropping = df.shape[0]

    # saveDroppedAS
    if saveDroppedAs is not None:
        # need to save the drops
        drops = df[df[studentId].isin(studentsToDrop)]
        # see http://pandas.pydata.org/pandas-docs/stable/io.html
        print("Saving raw data of dropped students to file '" + saveDroppedAs + "'")
        filename, ext = os.path.splitext(saveDroppedAs)
        if ext.lower() == ".csv":
            drops.to_csv(saveDroppedAs, encoding='utf-8')
        elif ext.lower() == ".pickle":
            drops.to_pickle(saveDroppedAs)
        else:
            warnings.warn("Unrecognized file extension '" + ext +
                          "' in the 'saveDroppedAs' parameter." +
                          "Dropped data are not saved.")

    df = df[-df[studentId].isin(studentsToDrop)]
    if verbose:
        print("After dropping dropping affected students:")
        print("Total number of evens in df     = %s" % (df.shape[0]))
        print("Total number of students in df  = %s" % (df[studentId].unique().shape[0]))
        print("Total number of evens dropped   = %s" % (sizeBeforeDropping - df.shape[0]))
        print("Total number of Students droped = %s" % (studentsToDrop.size))

    return df
