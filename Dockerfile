FROM python:3.12-alpine

COPY requirements.txt /temp/requirements.txt

EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev
RUN apk upgrade --update-cache --available && \
    apk add openssl && \
    rm -rf /var/cache/apk/*

RUN pip install -r /temp/requirements.txt

WORKDIR /code
COPY . /code
