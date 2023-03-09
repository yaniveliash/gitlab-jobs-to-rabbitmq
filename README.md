## Backend listener from gitlab

Listening on port 8080
Acceping GET requests with 5 payloads

- job_id
- project_id
- job_name
- project_name
- runner_id

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

services/web_listener
Amend the script path


## Backend message consumer

- Grab message from RabbitMQ
- Curl Gitlab API
- Reformat data to json
- Ingest to Elasticsearch


## Gitlab variables
- CI_JOB_ID
- CI_PROJECT_ID
- CI_RUNNER_ID


## Docker

Change the following if needed:
- Username
- Password
- Default VHOST
- RabbitMQ Hostname