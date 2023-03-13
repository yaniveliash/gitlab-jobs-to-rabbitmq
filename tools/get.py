import json
import logging
import requests
from tools import es
from tools import cli
from tools import connect
import re


args = cli.queue()
connection, channel = connect.rabbitmq(args.rabbit_user, args.rabbit_pass,
                                       args.rabbit_host, args.rabbit_port,
                                       args.rabbit_vhost)


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


def validateMandatoryFields(payload):
    mandatory_keys = ['gitlab_token', 'index_name', 'project_id', 'job_id',
                      'url']
    for key in payload.keys():
        if key in mandatory_keys and payload[key] == '':
            return False
    return True


def validateIndexName(index_name):
    pattern = r'^[A-Za-z][A-Za-z0-9-]*$'
    return bool(re.match(pattern, index_name))


# Define a callback function to handle incoming messages
def callback(ch, method, properties, rabbit_message: str):
    payload = json.loads(rabbit_message)
    valid_message = validateMandatoryFields(payload)
    valid_message = validateIndexName(payload['index_name'])

    if not valid_message:
        logging.info("Received invalid message - dropping")
        channel.basic_reject(delivery_tag=method.delivery_tag,
                             requeue=False)
    else:
        logging.info("Received valid message")
        job_console_output = getJobConsole(payload)
        try:
            es.ingest(job_console_output, payload)
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception:
            channel.basic_nack(delivery_tag=method.delivery_tag,
                               multiple=False, requeue=True)
            logging.error('Message ingestion to Elasticsearch failed.')


def getMessage():
    # Start consuming messages from the queue
    channel.basic_consume(queue=args.rabbit_queue,
                          on_message_callback=callback,
                          auto_ack=False)
    channel.start_consuming()
