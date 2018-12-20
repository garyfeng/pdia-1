import logging

# flag for logging
# if true, use multiprocessing logging: https://docs.python.org/2/library/multiprocessing.html#logging
# if false, use the default pdia logging in pdia.logger
isMultiprocessing = False

if isMultiprocessing:
    import multiprocessing
    logger = multiprocessing.log_to_stderr()
else:
    logger = logging.getLogger('pdia')

    # create file handler which logs even debug messages
    #fh = logging.FileHandler('writing2016.log')
    #fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    #logger.addHandler(fh)
    logger.addHandler(ch)

# config 2 log handlers
logger.setLevel(logging.INFO)

