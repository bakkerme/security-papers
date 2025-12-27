FROM python:3.11.14-alpine3.23

RUN apk add --no-cache python3 py3-pip tzdata bash

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY security_papers ./security_papers
COPY entrypoint.sh /entrypoint.sh
COPY run-job.sh /usr/local/bin/run-job.sh

RUN chmod +x /entrypoint.sh /usr/local/bin/run-job.sh

ENV PYTHONUNBUFFERED=1

VOLUME ["/data"]

ENTRYPOINT ["/entrypoint.sh"]
