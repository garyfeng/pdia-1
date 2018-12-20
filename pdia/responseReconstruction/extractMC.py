import io
import json, string
import traceback

from pdia import logger
from pdia.extendedInfoParser.parseJSON import parseJsonDatum
from pdia.responseReconstruction.num2alpha import num2alpha

# MCSS & MCMS
# MCSS = """
# {'Response': [{'Eliminations': [],
#    'Index': 0,
#    'OtherInfo': [],
#    'Response': [{'Index': 0,
#      'OtherInfoTextExist': False,
#      'Selected': False,
#      'val': ''},
#     {'Index': 1,
#      'OtherInfoTextExist': False,
#      'Selected': False,
#      'val': ''},
#     {'Index': 2,
#      'OtherInfoTextExist': False,
#      'Selected': False,
#      'val': ''},
#     {'Index': 3, 'Selected': True, 'val': 4}]}]}
# """
#
# MCMS = """
# {'Response': [{'Eliminations': [],
#    'Index': 0,
#    'OtherInfo': [],
#    'Response': [{'Index': 0, 'Selected': False, 'val': ''},
#     {'Index': 1, 'Selected': True, 'val': 2},
#     {'Index': 2,
#      'OtherInfoTextExist': False,
#      'Selected': False,
#      'val': ''},
#     {'Index': 3, 'Selected': True, 'val': 4}]}]}
# """


def extractMC(s, maxNumberOfOptions = 10):
    """
    Function extract MC responses from a string with response JSON, and returns the MC resposnes as an array of arrays.

    Each MC has 1 "records" which may have one or more "Selected==True" depending on SS or MS variant.
    The result will be an array of arrays, with each element being a response record.

    The input format is something like this:

    u'{"Response":[{"Index":0,"Response":[{"Index":0,"val":"","Selected":false},
    {"Index":1,"val":"","Selected":false},{"Index":2,"val":3,"Selected":true}],"Eliminations":[]}]}'

    The output is ["C"]. Note that if 'OtherInfoTextExist' is True for a record, the answer is the 'OtherInfo' field
    from the top Response object.

    If no response, return [].
    If not a response string, return None
    If "selected" is marked as True but no "val", then an "X" is added as reponse

    :param s: the json structure with responses
    :param maxNumberOfOptions: optional the max number of options for MC; default to 10 to save space
    :return: answer string
    """

    answerlist=[]
    try:
        # RespDict = json.loads(s)
        # handle cases where s is already a JSON object
        RespDict = parseJsonDatum(s)
        for records in RespDict["Response"]:
            for record in records["Response"]:
                if record["Selected"] is True:
                    # simplified output
                    if record["val"]=="":
                        try:
                            if record['OtherInfoTextExist'] is True:
                                answerlist.append(records['OtherInfo'])
                        except KeyError:
                            answerlist.append('X')
                    else:
                        value = int(record['val'])
                        v = num2alpha(value)
                        answerlist.append(v)
    except:
        return None
    return answerlist


def extractMCResponse(respList, maxNumberOfOptions=10):
    """
    This function extracts MC responses from the XML output, and returns a list of options in letters (and numbers if
    out of range).

    The input is of the following format:

    [{u'val': u'true', u'key': u'4'}]

    The output of the above would be ["D"].

    If no response, return [].
    If not a response string, return None

    :param respList: the json structure with responses
    :param maxNumberOfOptions: optional the max number of options for MC; default to 10 to save space
    :return: answer string
    """

    try:
        res = [num2alpha(r["key"]) for r in respList]
    except Exception as e:
        logger.error("extractMCResponse:")
        logger.exception(e)
        exc_buffer = io.StringIO()
        traceback.print_exc(file=exc_buffer)
        logger.error('Uncaught exception in worker process:\n%s', exc_buffer.getvalue())

        res = respList

    return res