from tools import connect
from tools.get import getMessage
import sys
import signal
from tools.error import error
from tools import cli


def signal_handler(sig, frame):
    print('Received SIGINT, shutting down gracefully...')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

args = cli.queue()

try:
    connection, channel = connect.rabbitmq(args.rabbit_user, args.rabbit_pass,
                                           args.rabbit_host, args.rabbit_port,
                                           args.rabbit_vhost)
except Exception:
    error('Error connecting to RabbitMQ')

getMessage(channel, args)
# try:
#     getMessage(channel, args)
# except Exception:
#     error('Error getting messages from RabbitMQ')

# Close the connection
connection.close()
