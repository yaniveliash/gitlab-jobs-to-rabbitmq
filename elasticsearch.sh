docker network create elastic

docker run -d \
--name elasticsearch \
--net elastic \
-p 9200:9200 \
docker.elastic.co/elasticsearch/elasticsearch:8.6.2

# To reset elastic user password
# docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
