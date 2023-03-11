## What is this project about

I could't find a way to ingest console output of gitlab pipelines,
and so I decided to use the existing gitlab API to grab console outputs
based on project ID and job ID, transform the data and ingest it to Elasticsearch
for further analysis.

The concept is pretty simple:
There is a webserver that listen for incoming GET request with query payload
for each pipeline that we want to ingest there is an `after_script` that simple curl
our webserver endpoint with the relevant payload.

The webserver transform that data into JSON and ship it to RabbitMQ as a message.

A consumer listen on that queue and invoke API call back to Gitlab with the constructed
API URL to grab the particular job console output.

It then transform each line from the console output into an Elasticsearch document and ship it to the cluster.


## Web listener from gitlab
`web_listener.py`

Listening on port 8080
Acceping 5 URL Query payload:

- job_id
- project_id
- job_name
- project_name
- runner_id
- gitlab_token

> I'm well aware that publishing gitlab_token as plain text is a big NO-NO, feel free to PR SSL support.

Pushing directly to rabbitMQ queue

Possible flags:
```
  -h, --help            show this help message and exit
  -p PORT               The port to listen on [Default: 8080]
  --user RABBIT_USER    RabbitMQ Username
  --pass RABBIT_PASS    RabbitMQ Password
  --host RABBIT_HOST    RabbitMQ Host
  --port RABBIT_PORT    RabbitMQ Port [Default: 5672]
  --vhost RABBIT_VHOST  RabbitMQ VHost [Default: my_vhost]
  --exchange RABBIT_EXCHANGE
                        RabbitMQ Exchange [Default: gitlab_jobs]
  --routekey RABBIT_ROUTE_KEY
                        RabbitMQ Exchange Routing Key [Default: jobs]
  --gitlab GITLAB_URL   Gitlab Base URL [Default: https://gitlab.com/]
  --debug               enable debug mode
```

**Service**

- services/web_listener
- services/queue_listener


## Message consumer
`queue_listener.py`

- Grab message from RabbitMQ
- Curl Gitlab API
- Reformat data to json
- Ingest to Elasticsearch

```
  -h, --help            show this help message and exit
  --rmq-user RABBIT_USER
                        RabbitMQ Username
  --rmq-pass RABBIT_PASS
                        RabbitMQ Password
  --rmq-host RABBIT_HOST
                        RabbitMQ Host
  --rmq-port RABBIT_PORT
                        RabbitMQ Port [Default: 5672]
  --rmq-vhost RABBIT_VHOST
                        RabbitMQ VHost [Default: my_vhost]
  --rmq-queue RABBIT_QUEUE
                        RabbitMQ Queue Name [Default: jobs]
  --es-host ES_HOST     Elasticsearch Hostname
  --es-port ES_PORT     Elasticsearch port [Default: 9200]
  --es-user ES_USER     Elasticsearch Username [Default: elastic]
  --es-pass ES_PASS     Elasticsearch Password for user 'elastic'
  --es-index ES_INDEX   Elasticsearch Index name where today's date [YYYY-MM-DD-*] is always attached to input name
  --es-url-scheme ES_URL_SCHEME
                        Elasticsearch URL scheme [http/https] [Default: https]
  --es-verify-ssl ES_SSL_NOVERIFY
                        Elasticsearch ignore self-signed SSL certificates [Default: False]
  --debug               enable debug mode
```


## Gitlab

We are interested in the following variables
- CI_PROJECT_ID
- CI_RUNNER_ID
- CI_JOB_ID
- CI_JOB_NAME
- CI_PROJECT_NAME
- GITLAB_TOKEN

At the after_script you will need to execute the following:
```
curl http://$LISTENER_HOST:$PORT/?project_id=${CI_PROJECT_ID}&runner_id=${CI_RUNNER_ID}&job_id={$CI_JOB_ID}&job_name=${CI_JOB_NAME}&project_name=${CI_PROJECT_NAME}&gitlab_token=${GITLAB_TOKEN}
```


## Docker

I've added a few examples for the following services:
- RabbitMQ
- Elasticsearch
- Kibana

> These are just examples for testing, amend those to meet your requirements, needs and production readyness.

## How to Run

First spin up RabbitMQ in docker, amend the values as needed
> Note that there is no persistant volume, you will need to mount `-v 'HOST_PATH_TO_RABBITMQ_LOCAL/data:/var/lib/rabbitmq/mnesia/'`

Now spin up Elasticsearch (see notes in the shell script) and next Kibana.

Next, initialize your new RabbitMQ using `initRabbitMQ.py`
> Elasticsearch does not need initialization

Now spin up the consumer as a service using `queue_listener.py`

And last, spin up the web server to accept calls from gitlab using `web_listener.py`

Now using an `after_script` in gitlab pipeline add a curl call as described above in this readme.

I recommend adding monitoring on your services and enabling SSL for the communication.
