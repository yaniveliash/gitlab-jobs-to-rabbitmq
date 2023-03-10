from tools.connect import connect
from tools.get import getMessage
import argparse
import sys
import signal
from tools.error import error


def signal_handler(sig, frame):
    print('Received SIGINT, shutting down gracefully...')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Initialize RabbitMQ for \
                                 receiving messages from Gitlab jobs.')
parser.add_argument('--user', dest='rabbit_user', type=str,
                    required=True, help='RabbitMQ Username')
parser.add_argument('--pass', dest='rabbit_pass', type=str,
                    required=True, help='RabbitMQ Password')
parser.add_argument('--host', dest='rabbit_host', type=str,
                    required=True, help='RabbitMQ Host')
parser.add_argument('--port', dest='rabbit_port', type=int,
                    default=5672, help='RabbitMQ Port [Default: 5672]')
parser.add_argument('--vhost', dest='rabbit_vhost', type=str,
                    default='my_vhost', help='RabbitMQ VHost \
                        [Default: my_vhost]')
parser.add_argument('--queue', dest='rabbit_queue', type=str,
                    default='jobs', help='RabbitMQ Queue Name \
                        [Default: jobs]')
parser.add_argument('--debug', action='store_true', help='enable debug mode')

args = parser.parse_args()

try:
    connection, channel = connect(args.rabbit_user, args.rabbit_pass,
                                  args.rabbit_host, args.rabbit_port,
                                  args.rabbit_vhost)
except Exception:
    error('Error connecting to RabbitMQ')

try:
    getMessage(channel, args.rabbit_queue, args.debug)
except Exception:
    error('Error getting messages from RabbitMQ')

# Close the connection
connection.close()
