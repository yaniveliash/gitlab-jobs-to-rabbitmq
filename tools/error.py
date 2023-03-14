import traceback
import logging
import sys


def error(msg):
    logging.error(f'{msg}')
    logging.error(traceback.format_exc())
    sys.exit(1)
