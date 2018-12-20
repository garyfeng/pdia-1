import io
import traceback

from pdia import logger


def extractTextSelectionResponse(respList):
    """
    Extract response from TextSelection item types in SBTS.

    Example:
        [{u'val': u'3', u'key': u'selectedUnit1'}] --> [selection-3]

    :param respList: the json structure with responses
    :param maxNumberOfOptions: optional the max number of options for MC; default to 10 to save space
    :return: answer string
    """
    try:
        res = ["selection-" + r["val"] for r in respList]
    except Exception as e:
        logger.error("extractTextSelectionResponse:")
        logger.exception(e)
        exc_buffer = io.StringIO()
        traceback.print_exc(file=exc_buffer)
        logger.error('Uncaught exception in worker process:\n%s', exc_buffer.getvalue())

        res = respList

    return res
