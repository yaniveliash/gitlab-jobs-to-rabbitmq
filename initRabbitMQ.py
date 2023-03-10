from tools.connect import connect
from tools.init import init
import argparse
from rich import print
import logging


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
parser.add_argument('--exchange', dest='rabbit_exchange', type=str,
                    default='gitlab_jobs', help='RabbitMQ Exchange \
                        [Default: gitlab_jobs]')
parser.add_argument('--type', dest='rabbit_exchange_type', type=str,
                    default='direct', help='RabbitMQ Exchange Type \
                        [Default: direct]')
parser.add_argument('--durable', dest='rabbit_exchange_durable', type=bool,
                    default=True, help='RabbitMQ Exchange Durability \
                        [Default: True]')
parser.add_argument('--passive', dest='rabbit_exchange_passive', type=bool,
                    default=False, help='RabbitMQ Exchange Passive \
                        [Default: False]')
parser.add_argument('--routekey', dest='rabbit_route_key', type=str,
                    default='jobs', help='RabbitMQ Exchange Routing Key \
                        [Default: jobs]')
parser.add_argument('--queue', dest='rabbit_queue', type=str,
                    default='jobs', help='RabbitMQ Queue Name \
                        [Default: jobs]')
parser.add_argument('--debug', action='store_true', help='enable debug mode')

args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

try:
    connection, channel = connect(args.rabbit_user, args.rabbit_pass,
                                  args.rabbit_host, args.rabbit_port,
                                  args.rabbit_vhost)
except ValueError as e:
    print(f"Caught exception: {e}")

try:
    init(channel, args.rabbit_exchange, args.rabbit_exchange_type,
         args.rabbit_exchange_durable, args.rabbit_exchange_passive,
         args.rabbit_queue, args.rabbit_route_key)
except ValueError as e:
    print(f"Caught exception: {e}")

# Close the connection
connection.close()

if args.debug:
    logging.info('Initialized and created successfully.')
else:
    print('[green]Initialized and created successfully.[/green]')
