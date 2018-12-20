import numpy as np
import pandas as pd

# get global logger
# logger = logging.getLogger('pdia')

def durSinceBlockStart(x,
                       timestamp="EventTime",
                       durSinceBlockStart="durSinceBlockStart"):
    """
    Given a data frame of a single block of keystroke logs, add a column that is the duration 
    from the minimal timestamp, in seconds. In typical usage, we pass a df of a whole block, and
    get a duration column with the block start time as 0. 
    
    This does *not* resort the data; it simply
    calculates the duration from the minimal timestamp.
    
    :param x: the input data frame
    :param timestamp: the column name for the event time stamp
    :param durSinceBlockStart: the column name for the column to be added
    :return: the data frame with an added column of duration 
    """
    assert (isinstance(x, pd.DataFrame))
    # assert (blockId in x.columns)
    assert (timestamp in x.columns)

    x.loc[:, timestamp] = pd.to_datetime(x[timestamp])

    # if EventTime a string not a np.datetime
    # try:
    #    x.loc[:, timestamp] = pd.to_datetime(x[timestamp])
    # except:
    #   logger.error("Error durSinceBlockStart(): timestamp column cannot be converted to datetime")
    #   print ("Error durSinceBlockStart(): timestamp column cannot be converted to datetime")
    #   raise Exception("Error durSinceBlockStart(): timestamp column cannot be converted to datetime")

    # this works only because we have eliminated students with multipel runs of the same block
    # df.loc[:, blockStartTime] = df.groupby([studentId, blockId])[timestamp].transform(lambda x: x.head(1))
    # df.loc[:, blockStartTime] = df[timestamp].min()

    x.loc[:, durSinceBlockStart] = (x[timestamp] - x[timestamp].min()) / np.timedelta64(1, 's')

    return x
