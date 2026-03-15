import inspect
import logging


def func_logger():

    log_name = inspect.stack()[1][3]
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler("/Users/dar99807537m-h/PycharmProjects/AutomationFramework/reports/Script.log")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s', datefmt='%d/%m/%y %I:%M:%S %p %A')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
