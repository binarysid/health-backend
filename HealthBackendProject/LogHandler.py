import logging

def getLogHandler(filename):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '[%(asctime)s]: %(levelname)s: %(name)s: %(funcName)s: %(filename)s: line no- %(lineno)s : %(message)s')
    fileHandler = logging.FileHandler(filename)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    return logger