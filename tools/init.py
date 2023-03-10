def init(channel, exchange_name, exchange_type, durable, passive, queue_name,
         routing_key):
    # Create an exchange only if it doesn't exist

    channel.exchange_delete(exchange=exchange_name)

    try:
        channel.exchange_declare(
            exchange=exchange_name, exchange_type=exchange_type,
            durable=durable, passive=passive)
    except Exception as e:
        raise ValueError("Error in function1") from e

    # Check if the queue exists
    queue_declare = channel.queue_declare(
        queue=queue_name, durable=True, exclusive=False, auto_delete=False)
    queue_exists = queue_declare.method.message_count > 0

    # Create the queue if it doesn't exist
    if not queue_exists:
        channel.queue_declare(queue=queue_name, durable=True,
                              exclusive=False, auto_delete=False)

    # Bind the queue to the exchange
    channel.queue_bind(exchange=exchange_name, queue=queue_name,
                       routing_key=routing_key)