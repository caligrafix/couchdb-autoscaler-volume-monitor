# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

RUN apt update && apt install -y \
	curl \
	unzip \
	&& curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
	&& unzip awscliv2.zip \
	&& ./aws/install

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "main.py"]

CMD ["--volume-monitor"]