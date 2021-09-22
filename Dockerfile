# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
COPY ./run_scenario.sh ./run_scenario.sh
RUN chmod +x ./run_scenario.sh

ENTRYPOINT ["./run_scenario.sh"]