FROM python:3.12-alpine

COPY requirements.txt /temp/requirements.txt

EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev
RUN apt-get update && apt-get install -y openssl

RUN pip install -r /temp/requirements.txt

WORKDIR /code
COPY . /code
