import json
from rich import print
import logging
import requests


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def getJobConsole(payload):
    logging.info(f'Trying to grab {payload["url"]}')
    headers = {'PRIVATE-TOKEN': payload['gitlab_token']}
    response = requests.get(payload['url'], headers=headers)

    if response.status_code != 200:
        logging.error(f'{response.content.decode("utf-8")}')

    return response.content


# Define a callback function to handle incoming messages
def callback(ch, method, properties, message: str):
    payload = json.loads(message)
    logging.info('Got new message')
    if debug:
        print(payload)
    job_console_output = getJobConsole(payload)
    print(job_console_output)


def getMessage(channel, queue_name: str, d: bool):
    global debug
    debug = d
    # Start consuming messages from the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback,
                          auto_ack=True)
    channel.start_consuming()
