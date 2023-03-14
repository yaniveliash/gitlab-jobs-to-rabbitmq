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

> This tool is intended for internal networks use (e.g. self-hosted gitlab)


## Web listener from gitlab
`web_listener.py`

- Listening on port 8080 by default
- Acceping 5 URL Query payload
- Jsonfy query
- Ship message to RabbitMQ

### Web listener endpoints

- /?
  - print on script the mandatory params
- / 
  - result in 404
- /healthcheck
  - check both elasticsearch and rabbitmq connections
- /healthcheck?elasticsearch OR /healthcheck?rabbitmq
  - check specific service

### Query Variables:

|Variable|Mandatory?|Notes|
|---|---|---|
|job_id|Yes|CI_JOB_ID in gitlab CI   |
|project_id|Yes|CI_PROJECT_ID in gitlab CI   |
|gitlab_token|Yes|Generate an API Read only token|
|index_name|Yes|Index name must start with A-Za-z and can include numbers or hyphen. A date will be automatically added as suffix INDEX_NAME[-$DATE]|
|job_name|   |   |
|project_name|   |   |
|runner_id|   |Very useful to identify problematic runners that have abnormal failed jobs|


### Possible flags:

```
  -h, --help            show this help message and exit
  -p PORT               The port to listen on [Default: 8080]
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
  --es-url-scheme ES_URL_SCHEME
                        Elasticsearch URL scheme [http/https] [Default: https]
  --es-verify-ssl ES_SSL_NOVERIFY
                        Elasticsearch ignore self-signed SSL certificates [Default: False]
  --debug               enable debug mode
```

## Service

- services/web_listener
- services/queue_listener


## Message consumer
`queue_listener.py`

- Grab message from RabbitMQ
- Curl Gitlab API
- Reformat data to json
- Ingest to Elasticsearch


### Possible flags:

```
  -h, --help            show this help message and exit
  -p PORT               The port to listen on [Default: 8080]
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
- ES_INDEX_NAME

It's easier to manage variables such as GITLAB_TOKEN and ES_INDEX_NAME in Gitlab CI Variables rather than hard code them in your pipeline.

At the after_script you will need to execute the following:

```
curl http://$LISTENER_HOST:$PORT/?project_id=${CI_PROJECT_ID}&runner_id=${CI_RUNNER_ID}&job_id={$CI_JOB_ID}&job_name=${CI_JOB_NAME}&project_name=${CI_PROJECT_NAME}&gitlab_token=${GITLAB_TOKEN}&index_name=${ES_INDEX_NAME}
```

> 💡 Python requests is a valid option too


## Docker

I've added a few examples for the following services:
- RabbitMQ
- Elasticsearch
- Kibana

> ⚠️ These are just examples for testing, amend those to meet your requirements, needs and production readyness.


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


## Known Issues

- No SSL support for requests from Gitlab CI pipeline to the web listener
- If one would like to work with Gitlab as SaaS there is no implementation for ACL
- Error messages are not very helpful (e.g. if elastic password is wrong the error message will be just connection error but not 401)
- There is no retry mechanism if Elasticsearch of RabbitMQ are unavailable
