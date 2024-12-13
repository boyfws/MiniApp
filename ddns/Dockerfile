FROM ubuntu:latest

RUN apt-get update && apt-get install -y curl && apt-get clean

WORKDIR /duckdns

COPY duck.sh /duckdns/duck.sh

RUN chmod +x /duckdns/duck.sh


