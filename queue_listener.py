from tools.get import getMessage
import sys
import signal


def signal_handler(sig, frame):
    print('Received SIGINT, shutting down gracefully...')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

getMessage()
