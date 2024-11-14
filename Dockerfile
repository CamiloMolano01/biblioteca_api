FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app

COPY .env.docker /code/.env