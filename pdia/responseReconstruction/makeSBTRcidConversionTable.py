import pandas as pd
import numpy as np
# check similarity
from difflib import SequenceMatcher
import warnings, random


def similarity(a, b):
    """
    check similarity between two items a and b
    :param a: item 1, could be a string or a list of numbers
    :param b: item 2, could be a string or a list of numbers
    :return: similarlity value
    """
    return SequenceMatcher(None, a, b).ratio()


def makeSBTRcidConversionTable_Text(df, samples=25):
    """
    Function to make a conversion table for ResponseComponentIds for SBTs.

    Some SBTs are not consistent in naming ResponseComponentIds for the response and process data. As
    a result, we can extract and reconstruct responses, but cannot match them with certainty, because
    the item identifier (namely the ResponseComponentId) is different.

    For CR text-based items, there is a straightforward solution, because assuming responses are fully
    extracted/reconstructed and they match, we can compare all pairs of extracted-reconstructed answers
    and find pairs with maximal similarity (if not identical). Note that this method assumes a 1:1
    correspondence between extracted and reconstructed items.

    This function does this, and return a Pandas data frame that can serve as a conversion table to translate
    RCIds from reconstructed items to extracted items. It also (a) gives warnings when there are different
    number of items on the two sides; (b) returns conversion table only for cases with both sides; (c) gives
    warnings for a few QC conditions and suggests that you re-run the function; (d) allows you to run the
    text similarity based on a sample of students.

    :param df: a data frame that is typically the output dfCompare from the xval function(s)
    :param samples: number of students to sample for comparing the text similarities; larger is better but slower
    :return: a data frame for RCId conversion; also printing warnings
    """

    selectedStudents = pd.Series(df.BookletNumber.unique()).sample(n=samples)
    sampled = df.BookletNumber.isin(selectedStudents)
    # now we concatenate n=sample responses for each item as a single string
    # s1 and s2 are pd.Series for Recon and Extracted sample answers
    # we add some junk characters to avoid similarity==1.0
    idxCR1 = df.ReconstructedAnswer.apply(
        lambda s: (("'val':" in str(s)) and ("'key':" not in str(s))))
    s1 = df.loc[sampled & idxCR1, :].groupby(["ResponseComponentId"]) \
        .apply(lambda d: d.ReconstructedAnswer.sum() + "11")
    idxCR2 = df.ExtractedAnswer.apply(
        lambda s: (("'val':" in str(s)) and ("'key':" not in str(s))))
    s2 = df.loc[sampled & idxCR2, :].groupby(["ResponseComponentId"]) \
        .apply(lambda d: d.ExtractedAnswer.sum() + "22")

    # create a similarity matrix
    z = np.zeros(shape=(s1.shape[0], s2.shape[0]))
    for i in range(s1.shape[0]):
        for j in range(s2.shape[0]):
            z[i, j] = similarity(s1.iloc[i], s2.iloc[j])

    #     similarity matrix, sorted to maximize the trace; need to ensure no ties in argmax()
    #     which is why we added some junk strings at the top to avoid 1.0 similarities
    #     print z
    #     print z[:, np.argmax(z, axis=1)]
    #     print z[np.argmax(z, axis=0), :]
    #     print np.argmax(z, axis=0)
    #     print np.argmax(z, axis=1)
    #     print s1.index[np.argmax(z, axis=0)]
    #     print s2.index[np.argmax(z, axis=1)]

    # create a df
    res = pd.DataFrame({"ResponseComponentId_recon": s1.index,
                        "ResponseComponentId_resp": s2.index[np.argmax(z, axis=1)],
                        "Similarity": z[:, np.argmax(z, axis=1)].diagonal()
                        })
    # QC warnings
    if res.Similarity.min() < 0.85:
        warnings.warn("The similarity metric is low for some items. Re-run the function to validate")
    # print warnings if we have non-matched RCIds.
    if z.shape[0] == z.shape[1]:
        pass
    elif z.shape[0] < z.shape[1]:
        junkRCIdList = s2.index[list(set(range(max(s1.shape[0], s2.shape[0]))) - set(np.argmax(z, axis=1)))]\
                    .tolist()
        warnings.warn("ResponseComponentId in ExtractedAnswer has no counterpart in ReconstructedAnswer: \n{}"
            .format(junkRCIdList))
        dfJunk = pd.DataFrame({
            "ResponseComponentId_recon": ["NoMatch_{:08x}".format(random.getrandbits(32)) for i in junkRCIdList],
            "ResponseComponentId_resp": junkRCIdList,
            "Similarity": 0 })
        res = pd.concat([res, dfJunk])
    elif z.shape[0] > z.shape[1]:
        junkRCIdList = s1.index[list(set(range(max(s1.shape[0], s2.shape[0]))) - set(np.argmax(z, axis=0)))]\
                    .tolist()
        warnings.warn("ResponseComponentId in ReconstructedAnswer has no counterpart in ExtractedAnswer: \n{}"
            .format(junkRCIdList))
        dfJunk = pd.DataFrame({
            "ResponseComponentId_recon": junkRCIdList,
            "ResponseComponentId_resp": ["NoMatch_{:08x}".format(random.getrandbits(32)) for i in junkRCIdList],
            "Similarity": 0})
        res = pd.concat([res, dfJunk])
    # test to see if the RCIds are unique
    if res.ResponseComponentId_recon.value_counts().max() > 1:
        warnings.warn(
            "The ResponseComponentId for reconstructed answeres are not unique. Re-run the function to validate")
    if res.ResponseComponentId_resp.value_counts().max() > 1:
        warnings.warn("The ResponseComponentId for extracted answeres are not unique. Re-run the function to validate")

    return res
