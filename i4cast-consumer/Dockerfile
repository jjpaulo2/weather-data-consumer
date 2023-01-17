FROM python:3.11-alpine

RUN apk update
RUN apk add build-base make

COPY ./i4cast_consumer /srv/i4cast_consumer
COPY ./requirements.txt /srv/requirements.txt

RUN pip3 install -r /srv/requirements.txt --upgrade

WORKDIR /srv
ENV PYTHONPATH /srv

VOLUME [ "/srv/dist" ]