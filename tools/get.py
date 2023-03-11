import json
from rich import print
import logging
import requests
from tools import es


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def getJobConsole(payload):
    logging.info(f'Trying to grab {payload["url"]}')
    headers = {'PRIVATE-TOKEN': payload['gitlab_token']}
    response = requests.get(payload['url'], stream=True, headers=headers)

    if response.status_code != 200:
        logging.error(f'{response.content.decode("utf-8")}')

    return response.content


# Define a callback function to handle incoming messages
def callback(ch, method, properties, rabbit_message: str):
    payload = json.loads(rabbit_message)
    logging.info('Got new message')
    if args.debug:
        print(payload)
    job_console_output = getJobConsole(payload)
    es.ingest(args, job_console_output, payload)


def getMessage(channel, a):
    global args
    args = a
    # Start consuming messages from the queue
    channel.basic_consume(queue=args.rabbit_queue, on_message_callback=callback,
                          auto_ack=True)
    channel.start_consuming()
