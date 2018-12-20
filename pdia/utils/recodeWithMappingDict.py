import pandas as pd


def recodeWithMappingDict(df, fromCol, toCol, mapping,
                          errorMessage=None, overwrite=False,
                          verbose=True):
    """Takes a df, and a label column and a mapping dict, and returns a df with a new column
    with recoded data.

    :param df: Pandas data frame
    :param fromCol: a df column with discrete values to be recoded
    :param toCol: a df column that will be created or overwritten with the recoded values
    :param mapping: a dict that maps the fromCol to toCol
    :param errorMessage: [optional, default to None] error message for values not specified
            in the mapping function
    :param overwrite: [optional, default=False] If False, only code rows in which the values in
            the `fromCol` column match the keys specified in the mapping dict, leaving other rows
            in the `toCol` untouched. In the case `toCol` did not exist, this will create it and
            set non-matching values to `NaN`.
            If True, it tries to recode all rows in `fromCol`, setting
            unmatched rows in the `toCol` to `errorMessage`.
    :param verbose: [optional, default=True] to print a warning if `toCol` already exists in the df

    :returns: df with possibly a new column

    :example:
    >> recodeWithMappingDict(df, fromCol="Label", toCol="editorState",
    mapping={
        'Expand Prompt':{"editorState":"Split"},
        'Expand Response':{"editorState":"Split"},
        'Collapse Response':{"editorState":"ResponseOnly"},
        'Collapse Prompt':{"editorState":"PromptOnly"}
    },
    errorMessage = {"editorState":"Unknown"},
    overwrite=True)
    >>
    """

    assert (isinstance(df, pd.DataFrame))
    assert (fromCol in df.columns)
    assert (isinstance(toCol, str))
    assert (isinstance(mapping, dict))

    if overwrite is True:
        # make sure mapping has all the events
        labels = df[fromCol].unique()
        for l in list(set(labels) - set(mapping.keys())):
            mapping[l] = errorMessage
        if verbose is True and toCol in df.columns:
            print("Warning recodeWithMappingDict(): \'{0}\' already exists and will be overwritten.".format(toCol))
        df.loc[:, toCol] = df[fromCol].apply(lambda x: mapping[x])
    else:
        # only change rows that match the mapping keys; create a new toCol if necessary
        matched = df[fromCol].isin(list(mapping.keys()))
        df.loc[matched, toCol] = df.loc[matched, fromCol].apply(lambda x: mapping[x])

    return df