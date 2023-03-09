# Define a callback function to handle incoming messages
from rich import print


def callback(ch, method, properties, body):
    body = body.decode('utf-8')
    print(f'[cyan]Received message:[/cyan] {body}')


def getMessage(channel, queue_name):
    # Start consuming messages from the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, 
                          auto_ack=True)
    channel.start_consuming()