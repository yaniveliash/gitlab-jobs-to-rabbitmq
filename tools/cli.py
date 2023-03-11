import argparse

# Default Variables:
web_port = 8080

rabbit_port = 5672
rabbit_vhost = 'my_vhost'
rabbit_exchange = 'gitlab_jobs'
rabbit_routing_key = 'jobs'
rabbit_queue = 'jobs'

gitlab_url = 'https://gitlab.com/'

es_user = 'elastic'
es_port = 9200
es_url_scheme = 'https'
es_verify_ssl = False


def web():
    parser = argparse.ArgumentParser(description='Start a web \
                                     server to handle GET requests \
                                     from Gitlab pipelines which are \
                                     being posted to RabbitMQ for further \
                                    processing.')
    parser.add_argument('-p', dest='port', type=int, default=web_port,
                        help=f'The port to listen on [Default: {web_port}]')
    parser.add_argument('--user', dest='rabbit_user', type=str,
                        required=True, help='RabbitMQ Username')
    parser.add_argument('--pass', dest='rabbit_pass', type=str,
                        required=True, help='RabbitMQ Password')
    parser.add_argument('--host', dest='rabbit_host', type=str,
                        required=True, help='RabbitMQ Host')
    parser.add_argument('--port', dest='rabbit_port', type=int,
                        default=rabbit_port, help=f'RabbitMQ Port \
                            [Default: {rabbit_port}]')
    parser.add_argument('--vhost', dest='rabbit_vhost', type=str,
                        default=rabbit_vhost, help=f'RabbitMQ VHost \
                            [Default: {rabbit_vhost}]')
    parser.add_argument('--exchange', dest='rabbit_exchange', type=str,
                        default=rabbit_exchange, help=f'RabbitMQ Exchange \
                            [Default: {rabbit_exchange}]')
    parser.add_argument('--routekey', dest='rabbit_route_key', type=str,
                        default=rabbit_routing_key, help=f'RabbitMQ Exchange \
                            Routing Key [Default: {rabbit_routing_key}]')
    parser.add_argument('--gitlab', dest='gitlab_url', type=str,
                        default=gitlab_url, help=f'Gitlab Base URL \
                            [Default: {gitlab_url}]')
    parser.add_argument('--debug', action='store_true',
                        help='enable debug mode')

    return parser.parse_args()


def queue():
    parser = argparse.ArgumentParser(description='Initialize RabbitMQ for \
                                 receiving messages from Gitlab jobs.')
    parser.add_argument('--rmq-user', dest='rabbit_user', type=str,
                        required=True, help='RabbitMQ Username')
    parser.add_argument('--rmq-pass', dest='rabbit_pass', type=str,
                        required=True, help='RabbitMQ Password')
    parser.add_argument('--rmq-host', dest='rabbit_host', type=str,
                        required=True, help='RabbitMQ Host')
    parser.add_argument('--rmq-port', dest='rabbit_port', type=int,
                        default=rabbit_port, help=f'RabbitMQ Port \
                            [Default: {rabbit_port}]')
    parser.add_argument('--rmq-vhost', dest='rabbit_vhost', type=str,
                        default=rabbit_vhost, help=f'RabbitMQ VHost \
                            [Default: {rabbit_vhost}]')
    parser.add_argument('--rmq-queue', dest='rabbit_queue', type=str,
                        default=rabbit_queue, help=f'RabbitMQ Queue Name \
                            [Default: {rabbit_queue}]')
    parser.add_argument('--es-host', dest='es_host', type=str, required=True,
                        help='Elasticsearch Hostname')
    parser.add_argument('--es-port', dest='es_port', type=str, default=es_port,
                        help=f'Elasticsearch port [Default: {es_port}]')
    parser.add_argument('--es-user', dest='es_user', default=es_user,
                        type=str, help=f'Elasticsearch Username \
                            [Default: {es_user}]')
    parser.add_argument('--es-pass', dest='es_pass', type=str, required=True,
                        help='Elasticsearch Password for user \'elastic\'')
    parser.add_argument('--es-index', dest='es_index', type=str, required=True,
                        help='Elasticsearch Index name where today\'s date \
                            [YYYY-MM-DD-*] is always attached to input name')
    parser.add_argument('--es-url-scheme', dest='es_url_scheme', type=str,
                        default=es_url_scheme, help=f'Elasticsearch URL \
                            scheme [http/https] [Default: {es_url_scheme}]')
    parser.add_argument('--es-verify-ssl', dest='es_ssl_noverify', type=bool,
                        default=es_verify_ssl, help=f'Elasticsearch ignore \
                            self-signed SSL certificates \
                            [Default: {es_verify_ssl}]')
    parser.add_argument('--debug', action='store_true',
                        help='enable debug mode')

    return parser.parse_args()


def rabbitInit():
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

    return parser.parse_args()
