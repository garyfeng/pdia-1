import os
import warnings

import numpy as np
import pandas as pd


def findDuplicatedEvents(df, keys=['BookletNumber', 'BlockCode', 'AccessionNumber', 'Label',
                                   'EventTime', 'ExtendedInfo'],
                         deltaTime=None,
                         timeStampColumn='EventTime',
                         saveDuplicatesAs=None,
                         verbose=True):
    """Find any duplicated events, optionally save the duplicated.

    Takes a df, finds dups by 'keys' and returns the duplicated rows (both copies)
    Optional deltaTime: if consequtive EventTime's deltaTime is smaller than deltaTime,
    and everything else are the same, we consider them the same.

    :type timeStampColumn: str
    :param timeStampColumn: name of the timestamp column; default to 'EventTime'
    :type keys: list
    :param keys: a list of column names with which to find duplicated records
    :type saveDuplicatesAs: str
    :param saveDuplicatesAs: file name to save the duplicated events

    :return: data frame containing duplicated rows; None if no duplications
    """

    # error checks
    assert (isinstance(df, pd.DataFrame))
    for v in keys:
        assert (v in df.columns)

    # first find the index for the dups; keeping all members of dups
    if deltaTime is None:
        # first check for duplicates, and print out a sample if there are
        # Note that we keep both copies here, in order to show the dups
        isDup = df.duplicated(keys, keep=False)
    else:
        # deltaTime is the time threshold, in milliseconds
        # get indecies of "close" events; remember to get both members of the pair
        #   i.e., calc the deltaTime from the Prev and Next events; keeping both
        deltaTime = np.timedelta64(deltaTime * 1000000)

        dt = df[timeStampColumn].diff()
        idx = np.logical_and(dt >= np.timedelta64(0), dt < deltaTime)
        df.loc[idx, timeStampColumn] = df[timeStampColumn].shift()[idx]

        newKeys = list(set(keys) | {timeStampColumn})
        isDup = df.duplicated(newKeys, keep=False)

    # isDup is the index for dup items, with both members of the pairs
    dup = df.loc[isDup, :]

    if verbose:
        print("Total number of duplicated events  = %s" % (dup.shape[0]))

    # if there is data
    if dup.shape[0] > 0:
        if saveDuplicatesAs is not None:
            if verbose:
                print("Saving duplicated events to %s" % (str(saveDuplicatesAs)))
            # need to save the dups
            # see http://pandas.pydata.org/pandas-docs/stable/io.html
            filename, ext = os.path.splitext(saveDuplicatesAs)
            if ext.lower() == ".csv":
                dup.to_csv(saveDuplicatesAs, encoding='utf-8')
            elif ext.lower() == ".pickle":
                dup.to_pickle(saveDuplicatesAs)
            else:
                warnings.warn("Unrecognized file extension '" + ext
                              + "' in the 'saveDuplicatesAs' parameter." + "Duplicated data are not saved.")
        return dup
    else:
        return None


def dropDuplicatedEvents(df, keys=['BookletNumber', 'BlockCode', 'AccessionNumber', 'Label',
                                   'EventTime', 'ExtendedInfo'],
                         deltaTime=None,
                         timeStampColumn='EventTime',
                         saveDuplicatesAs=None,
                         verbose=True):
    """
    Takes a df, finds duplications by 'keys' and keeps only the first instance if drop==True.

    If drop==False,
    it returns the duplicated rows (both copies) if there are dups else the df.
    This behavior is not totally intuitive but this is a rare use case

    :param df: the input data frame, which can include multiple booklets and blocks
    :param keys: a list of column names; rows with identical values across these columns are considered duplicates
    :param deltaTime: the minimal time differences (in seconds) between events to be considered not duplicates. Default
    is None, in which case time is not a consideration. Otherwise consecutive events more than deltaTime apart are not
    considered as duplicates.
    :param timeStampColumn: the column name that is the timestamp; default to 'EventTime'
    :param saveDuplicatesAs: default to None; If a filename is passed, it will save the duplicated records to the file
    :param verbose: default to True; it prints out the number of records before and after the drop.
    :return:
    """

    # error checks
    assert (isinstance(df, pd.DataFrame))
    for v in keys:
        assert (v in df.columns)

    if verbose:
        print("\ndropDuplicatedEvents:")

    # only if we want to save the dups
    if saveDuplicatesAs is not None:
        dup = findDuplicatedEvents(df, keys=keys, deltaTime=deltaTime,
                                   timeStampColumn=timeStampColumn, saveDuplicatesAs=saveDuplicatesAs,
                                   verbose=verbose)

    sizeBeforeDropping = df.shape[0]
    # now let's find the dups
    if deltaTime is not None:
        # deltaTime is the time threshold, in milliseconds
        # get indecies of "close" events; remember to get both members of the pair
        #   i.e., calc the deltaTime from the Prev and Next events; keeping both
        deltaTime = np.timedelta64(deltaTime * 1000000)

        dt = df[timeStampColumn].diff()
        idx = np.logical_and(dt >= np.timedelta64(0), dt < deltaTime)
        df.loc[idx, timeStampColumn] = df[timeStampColumn].shift()[idx]

        keys = list(set(keys) | {timeStampColumn})

    df = df.drop_duplicates(keys, keep="first")

    if verbose:
        print("Total number of evens before  = %s" % (sizeBeforeDropping))
        print("Total number of evens after   = %s" % (df.shape[0]))
        print("Total number of evens dropped = %s" % (sizeBeforeDropping - df.shape[0]))

    return df
