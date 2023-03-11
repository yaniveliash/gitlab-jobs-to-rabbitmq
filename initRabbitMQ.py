from tools import connect
from tools import init
from rich import print
import logging
from tools.error import error
from tools import cli


args = cli.rabbitInit()

if args.debug:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

try:
    connection, channel = connect.rabbitmq(args.rabbit_user, args.rabbit_pass,
                                           args.rabbit_host, args.rabbit_port,
                                           args.rabbit_vhost)
except Exception:
    error('Error connecting to RabbitMQ')

try:
    init.rabbitmq(channel, args.rabbit_exchange, args.rabbit_exchange_type,
         args.rabbit_exchange_durable, args.rabbit_exchange_passive,
         args.rabbit_queue, args.rabbit_route_key)
except Exception:
    error('Error initializing RabbitMQ')

# Close the connection
connection.close()

if args.debug:
    logging.info('Initialized and created successfully.')
else:
    print('[green]Initialized and created successfully.[/green]')
