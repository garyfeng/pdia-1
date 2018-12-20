import json


# BQChoice
# Note that this code does not recover "OtherInfo" text from each part.
sBQChoice = """
{'Response': [{'Index': 0,
   'OtherInfo': [],
   'OtherInfoTextExist': False,
   'PartId': 'VH271370',
   'Response': [{'Index': 0, 'Selected': False, 'val': ''},
    {'Index': 1, 'Selected': False, 'val': ''},
    {'Index': 2, 'Selected': False, 'val': ''},
    {'Index': 3, 'Selected': False, 'val': ''},
    {'Index': 4, 'Selected': True, 'val': 5}]},
  {'Index': 1,
   'OtherInfo': [],
   'OtherInfoTextExist': False,
   'PartId': 'VH271372',
   'Response': [{'Index': 0, 'Selected': False, 'val': ''},
    {'Index': 1, 'Selected': False, 'val': ''},
    {'Index': 2, 'Selected': True, 'val': 3},
    {'Index': 3, 'Selected': False, 'val': ''},
    {'Index': 4, 'Selected': False, 'val': ''}]},
  {'Index': 2,
   'OtherInfo': [],
   'OtherInfoTextExist': False,
   'PartId': 'VH271374',
   'Response': [{'Index': 0, 'Selected': False, 'val': ''},
    {'Index': 1, 'Selected': False, 'val': ''},
    {'Index': 2, 'Selected': False, 'val': ''},
    {'Index': 3, 'Selected': True, 'val': 4},
    {'Index': 4, 'Selected': False, 'val': ''}]},
  {'Index': 3,
   'OtherInfo': [],
   'OtherInfoTextExist': False,
   'PartId': 'VH271375',
   'Response': [{'Index': 0, 'Selected': False, 'val': ''},
    {'Index': 1, 'Selected': False, 'val': ''},
    {'Index': 2, 'Selected': False, 'val': ''},
    {'Index': 3, 'Selected': True, 'val': 4},
    {'Index': 4, 'Selected': False, 'val': ''}]}]}
"""

def parseBQChoice(s):
    """
    takes a string with response JSON, and returns the BQChoice resposnes as an array of arrays.
    Each BQChoice will have multiple objects with PartId.

    :param s: the json structure with responses
    :return: answer string
    """
    answerlist = []
    try:
        RespDict = json.loads(s)
        for records in RespDict["Response"]:
            for record in records["Response"]:
                if(record["Selected"] is True):
                    answerlist.append("{}-{}".format(records["PartId"], record["val"]))
    except:
        return None
    return answerlist