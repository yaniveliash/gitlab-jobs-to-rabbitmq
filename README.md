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

It then transform the data into json and ship it to Elasticsearch cluster.


## Backend listener from gitlab

Listening on port 8080
Acceping GET requests with 5 payloads

- job_id
- project_id
- job_name
- project_name
- runner_id
- gitlab_token

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
                        RabbitMQ Exchange [Default: gitlab_exchange]
  --routekey RABBIT_ROUTE_KEY
                        RabbitMQ Exchange Routing Key [Default: jobs]
  --gitlab GITLAB_URL   Gitlab Base URL [Default: https://gitlab.com/api/v4/projects/]
  --debug               enable debug mode
```

**Service**

- services/web_listener
- services/queue_listener


## Backend message consumer

- Grab message from RabbitMQ
- Curl Gitlab API
- Reformat data to json
- Ingest to Elasticsearch

```
  -h, --help            show this help message and exit
  --user RABBIT_USER    RabbitMQ Username
  --pass RABBIT_PASS    RabbitMQ Password
  --host RABBIT_HOST    RabbitMQ Host
  --port RABBIT_PORT    RabbitMQ Port [Default: 5672]
  --vhost RABBIT_VHOST  RabbitMQ VHost [Default: my_vhost]
  --queue RABBIT_QUEUE  RabbitMQ Queue Name [Default: jobs]
  --debug               enable debug mode
```


## Gitlab

We are interested in the following variables
- CI_PROJECT_ID
- CI_RUNNER_ID
- CI_JOB_ID
- CI_JOB_NAME
- CI_PROJECT_NAME

At the after_script you will need to execute the following:
```
curl http://$LISTENER_HOST:$PORT/?project_id=${CI_PROJECT_ID}&runner_id=${CI_RUNNER_ID}&job_id={$CI_JOB_ID}&job_name=${CI_JOB_NAME}&project_name=${CI_PROJECT_NAME}
```


## Docker

Change the following if needed:
- Username
- Password
- Default VHOST
- RabbitMQ Hostname