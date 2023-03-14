import pika
from elasticsearch import Elasticsearch


def rabbitmq(username: str, password: str, hostname: str,
             port: int, vhost_name: str):
    try:
        # Set up connection parameters
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(
            hostname, port, vhost_name, credentials)

        # Establish a connection to the RabbitMQ server
        connection = pika.BlockingConnection(parameters)
        return connection, connection.channel()
    except:
        return None, None


def elasticsearch(host: str, port: int, username: str, password: str,
                  scheme: str, ssl_noverify: bool):
    try:
        es = Elasticsearch(
            [''.join([scheme, '://', host, ':', str(port)])],
            http_auth=(username, password),
            verify_certs=ssl_noverify
        )
        return es
    except:
        return None
