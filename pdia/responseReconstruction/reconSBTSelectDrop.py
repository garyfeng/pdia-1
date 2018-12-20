import pandas as pd


def reconSBTSelectDrop(itemLog, accnum="ControlId", itemtype="Label"):
    """
    Given a Pandas data frame containing the log for one item, return the reconstructed response.

    :param itemLog: a data fram containing the log of a single Select.Drop item
    :param accnum: the column name that identifies items
    :param itemtype: the column name that identifies the item type
    :return: a Pandas series of the reconstructed responses.

    """
    assert (isinstance(itemLog, pd.DataFrame))
    assert("extInfo" in itemLog.columns)
    # only a single item
    assert (itemLog[accnum].nunique() == 1)
    # only a single item type
    assert (itemLog["ItemTypeCode"].nunique() == 1)

    try:
        res=[]
        itemLog =  itemLog\
            .loc[itemLog[itemtype]=="select.drop"]
        # track states by looping through all actions from the top, less the trailing CAs
        d={}
        for index, row in itemLog.iterrows():
            #res.append({'key':row["extInfo"]["object"], 'val':row["extInfo"]["to"]})
            d[row["extInfo"]["object"]] = row["extInfo"]["to"]

        for key,val in list(d.items()):
            res.append({'key':key,'val':val})
    except:
        res = []
    return res