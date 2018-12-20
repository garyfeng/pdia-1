import io
import traceback

from pdia import logger


def extractSelectionResponse(respList):
    """
    To extract responses from in-text selection item types in reading
    assessments.

    :param respList: the json structure with responses
    :return: answer string
    """
    try:
        # res = ["option-" + str(i + 1) for i, o in enumerate(respList) if o["val"] == "true"]
        # i is for the option number, 0-based
        # o is for whether this option is chosen
        res = [str(i + 1) for i, o in enumerate(respList) if o["val"] == "true"]
    except Exception as e:
        logger.error("extractSelectionResponse:")
        logger.exception(e)
        exc_buffer = io.StringIO()
        traceback.print_exc(file=exc_buffer)
        logger.error('Uncaught exception in worker process:\n%s', exc_buffer.getvalue())

        res = respList

    return res
