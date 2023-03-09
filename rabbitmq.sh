#!/bin/bash
docker run -d \
--name rabbitmq \
--hostname rabbitmq \
-e RABBITMQ_DEFAULT_USER=user \
-e RABBITMQ_DEFAULT_PASS=password \
-e RABBITMQ_DEFAULT_VHOST=my_vhost \
-p 5672:5672 \
-p 15672:15672 \
rabbitmq:3.11.10-management-alpine
