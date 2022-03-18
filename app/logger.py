import logging
import time
from config import settings


def configure_logging(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s][%(name)-10s][%(levelname)-7s] %(message)s')
    handler.setFormatter(formatter)
    logging.Formatter.converter = time.gmtime
    logger.addHandler(handler)
    logger.setLevel(settings.logging.level)

    return logger
