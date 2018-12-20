import numpy as np
import pandas as pd


def countVisits(item, value=None):
    """This function takes a pandas.Series of item tags, and an optional string for a specific tag
    and returns a numpy.ndarray of the same size as the input, which contains either
    1) a running count of unique transitions of item, if no target tag is given, or
    2) a running count of the numer of entries to a run of target tag

    :param item: a pandas Series of labels of events
    :param value: optional value of the item to keep track of
    :return: a running count of the unique values of items if value==None, or a running count of the specific value
    """
    # make sure item is a 1-D np array or a Pandas Series
    # if not isinstance(item, (pd.core.series.Series, np.ndarray) ):
    assert (isinstance(item, pd.core.series.Series))

    # create counter; this saves time, apparently
    count = np.zeros((item.size), dtype=np.int)

    if value is None:
        # not specified, then we track any time item changes value
        count[np.where(item != item.shift())] = 1
    else:
        # only when item==value
        count[np.where(np.logical_and(item != item.shift(), item == value))] = 1

    return count.cumsum()
