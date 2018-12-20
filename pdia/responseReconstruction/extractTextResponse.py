import io
import traceback

from pdia import logger


def extractTextResponse(respList):
    """
    Extract response from Text item types in SBTs.

    Example: 
        [{'key': "Explain message of xxxx",
          'val': 'XXXXX'}]
        -->
        [{'val': 'XXXXX'}]

    :param respList: the json structure with responses
    :return: answer string
    """
    try:
        res = [{'val': o["val"]} for o in respList]
    except Exception as e:
        logger.error("extractTextResponse:")
        logger.exception(e)
        exc_buffer = io.StringIO()
        traceback.print_exc(file=exc_buffer)
        logger.error('Uncaught exception in worker process:\n%s', exc_buffer.getvalue())

        res = respList

    return res
