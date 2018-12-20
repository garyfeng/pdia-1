import json

# BQMCSS & BQMCMS
# json can't load unicode strings.
# had to use ast: https://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-from-json
sBQMCSS = """
{'Response': [{'Eliminations': [],
   'Index': 0,
   'OtherInfo': [],
   'Response': [{'Index': 0,
     'OtherInfoTextExist': False,
     'Selected': False,
     'val': ''},
    {'Index': 1,
     'OtherInfoTextExist': False,
     'Selected': False,
     'val': ''},
    {'Index': 2,
     'OtherInfoTextExist': False,
     'Selected': False,
     'val': ''},
    {'Index': 3, 'Selected': True, 'val': 4}]}]}
"""

sBQMCMS = """
{'Response': [{'Eliminations': [],
   'Index': 0,
   'OtherInfo': [],
   'Response': [{'Index': 0, 'Selected': False, 'val': ''},
    {'Index': 1, 'Selected': True, 'val': 2},
    {'Index': 2,
     'OtherInfoTextExist': False,
     'Selected': False,
     'val': ''},
    {'Index': 3, 'Selected': True, 'val': 4}]}]}
"""


def parseBQMC(s):
    """
    takes a string with response JSON, and returns the MC resposnes as an array of arrays.
    Each MC has 1 "records" which may have one or more "Selected==True" depending on SS or MS variant.
    The result will be an array of arrays, with each element being a response record.
    If no response, return [].
    If not a response string, return None

    :param s: the json structure with responses
    :return: answer string

    """

    answerlist = []
    try:
        RespDict = json.loads(s)
        for records in RespDict["Response"]:
            for record in records["Response"]:
                if record["Selected"] is True:
                    answerlist.append(record["val"])
    except:
        return None
    return answerlist
