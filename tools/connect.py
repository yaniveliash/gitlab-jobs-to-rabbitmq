import pika


def connect(username, password, hostname, port, vhost_name):
    try:
        # Set up connection parameters
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(
            hostname, port, vhost_name, credentials)

        # Establish a connection to the RabbitMQ server
        connection = pika.BlockingConnection(parameters)
        return connection, connection.channel()
    except pika.exceptions.AMQPConnectionError as e:
        return str(e)
