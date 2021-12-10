FROM ubuntu:latest

RUN apt-get update --yes && \
	apt-get upgrade --yes && \
	apt-get install curl --yes && \
	apt-get install jq --yes 

COPY scripts /scripts

WORKDIR /scripts

RUN chmod +x *.sh


ENTRYPOINT ["./main.sh"]