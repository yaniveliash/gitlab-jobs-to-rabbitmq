import json
from tools import connect
import urllib3
from rich import print
import datetime
import logging


def ingest(args, console, payload):
    global es
    global index_name

    # Surpress Elasticsearch output
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Index name is always YYYY-MM-DD-$IndexName
    index_name = datetime.datetime.today().strftime('%Y-%m-%d') + '-' \
        + args.es_index

    es = connect.elasticsearch(args.es_host, args.es_port, args.es_user,
                               args.es_pass, args.es_url_scheme,
                               args.es_ssl_noverify)

    # If index missing, create it
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, settings={"number_of_shards": 1,
                                                      "number_of_replicas": 0})

    process(console.decode('utf-8'), payload)


def process(console, payload):
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
    shipIt(payload)


def shipIt(payload):
    bulk_data = []

    for obj in json.loads(payload):
        action = {"index": {"_index": index_name}}
        doc = obj
        bulk_data.append(action)
        bulk_data.append(doc)
    es.bulk(index=index_name, operations=bulk_data)

    logging.info('Loaded data to Elasticsearch')
