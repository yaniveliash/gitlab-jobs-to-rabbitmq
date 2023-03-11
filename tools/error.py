import traceback
import logging
from rich import print
import sys


def error(msg):
    print(f'[red]{msg}[/red]\n')
    logging.error(traceback.format_exc())
    sys.exit(1)
