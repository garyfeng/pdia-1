import pandas as pd


def reshapeAnswersToOneRow(dfResponses):
    """
    take an answer data frame where each item is a row, return a data frame where each student is a row and each
    column is a unique AccNum.

    In the case the data frame contains multiple blocks, the output data will contain all AccNums of all blocks,
    without a marker for blockId.

    :param dfResponses: the row-based data frame containing answers
    :return: a column-based data frame where each student is a row.
    """
    assert (isinstance(dfResponses, pd.DataFrame))
    assert (label in dfResponses.columns for label in ['AccessionNumber', "BookletNumber", "Answer"])
    return dfResponses.pivot(columns='AccessionNumber', index="BookletNumber", values="Answer")