def rabbitmq(channel, args):
    # Create an exchange only if it doesn't exist

    # args.rabbit_exchange,
    # args.rabbit_exchange_type,
    # args.rabbit_exchange_durable,
    # args.rabbit_exchange_passive,
    # args.rabbit_queue,
    # args.rabbit_route_key

    channel.exchange_delete(exchange=args.rabbit_exchange)

    try:
        channel.exchange_declare(
            exchange=args.rabbit_exchange,
            exchange_type=args.rabbit_exchange_type,
            durable=args.rabbit_exchange_durable,
            passive=args.rabbit_exchange_passive)
    except Exception as e:
        raise ValueError("Error in function") from e

    queues = [{'name': args.rabbit_queue, 'bind': True},
              {'name': 'healthcheck', 'bind': False}]

    for queue in queues:
        createQueue(channel, queue['name'])

        if queue['bind']:
            bindQueue(channel, queue['name'], args)


def createQueue(channel, queue_name):
    # Check if the queue exists
    queue_declare = channel.queue_declare(
        queue=queue_name, durable=True, exclusive=False, auto_delete=False)
    queue_exists = queue_declare.method.message_count > 0

    # Create the queue if it doesn't exist
    if not queue_exists:
        channel.queue_declare(queue=queue_name, durable=True,
                              exclusive=False, auto_delete=False)


def bindQueue(channel, queue_name, args):
    # Bind the queue to the exchange
    channel.queue_bind(exchange=args.rabbit_exchange, queue=queue_name,
                       routing_key=args.rabbit_route_key)
