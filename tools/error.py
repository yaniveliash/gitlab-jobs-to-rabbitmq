import traceback
from rich import print
import sys


def error(msg):
    print(f'[red]{msg}[/red]\n')
    traceback.print_exc()
    sys.exit(1)
