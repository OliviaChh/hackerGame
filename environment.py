from behave.model import Status
from director import setup, logger


def before_feature(context, feature):
    setup(context)
    logger.debug("environment setup")
