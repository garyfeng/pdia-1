import pandas as pd
from pdia.responseReconstruction.num2alpha import alpha2num

def reconSBTSelectChoice(itemLog, accnum="ControlId", itemtype="Label"):
    """
    Given a Pandas data frame containing the log for one item, return the reconstructed response.

    :param itemLog: a data fram containing the log of a single Select.Choice item
    :param accnum: the column name that identifies items
    :param itemtype: the column name that identifies the item type
    :return: a Pandas series of the reconstructed responses.

    """
    
#    print 'From reconSBTSelectChoice'
    
    assert (isinstance(itemLog, pd.DataFrame))
    assert("extInfo" in itemLog.columns)
    # only a single item
    assert (itemLog[accnum].nunique() == 1)
    # only a single item type
    assert (itemLog["ItemTypeCode"].nunique() == 1)

    # return the last content
    try:
        res=[]
        response = itemLog\
            .loc[itemLog[itemtype]=="select.choose"]\
            .iloc[-1].extInfo["to"] #\
            #.replace('option-', '')\
            #.replace('selection-', '')
#        res.append(response)
        res.append(alpha2num(response))
    except:
        res = []
    return res