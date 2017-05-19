import sys


def log(message):
    """
    simple wrapper for logging to stdout on heroku or local machine

    :param message: message to be logged
    :return: None
    """
    print str(message)
    sys.stdout.flush()
