docker run -d \
--name kibana \
--net elastic \
-p 5601:5601 \
docker.elastic.co/kibana/kibana:8.6.2

# To attach kibana to elasticsearch you need to enroll a token
# docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token --scope kibana

# After you enter the token you will need an OTP
# Run docker logs kibana to see it there