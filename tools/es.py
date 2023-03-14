import json
from tools import connect
import urllib3
import datetime
import logging
from tools import cli
import sys


args = cli.args()

try:
    es = connect.elasticsearch(args.es_host, args.es_port, args.es_user,
                               args.es_pass, args.es_url_scheme,
                               args.es_ssl_noverify)
except Exception:
    logging.error('Elasticsearch connection failed')
    sys.exit(1)


def ingest(console, payload):
    # Surpress Elasticsearch output
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Index name is always $IndexName-YYYY-MM-DD
    index_name = payload['index_name'] + '-' + \
        datetime.datetime.today().strftime('%Y-%m-%d')

    # If index missing, create it
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, settings={"number_of_shards": 1,
                                                      "number_of_replicas": 0})

    process(console.decode('utf-8'), payload, index_name)


def process(console, payload, index_name):
    docs = []
    for line in console.splitlines():
        doc = {'timestamp': ' '.join([datetime.datetime.utcnow().isoformat()]),
               'message': ' '.join([line]),
               'runner_id': ' '.join([payload['runner_id']]),
               'project_id': ' '.join([payload['project_id']]),
               'job_id': ' '.join([payload['job_id']]),
               'job_name': ' '.join([payload['job_name']]),
               'project_name': ' '.join([payload['project_name']]),
               'url': ' '.join([payload['url']])}
        docs.append(doc)

    # Convert the list of dictionaries to JSON
    payload = json.dumps(docs)
    shipIt(payload, index_name)


def shipIt(payload, index_name):
    bulk_data = []

    for obj in json.loads(payload):
        action = {"index": {"_index": index_name}}
        doc = obj
        bulk_data.append(action)
        bulk_data.append(doc)
    es.bulk(index=index_name, operations=bulk_data)

    logging.info('Data load to Elasticsearch was successful')
