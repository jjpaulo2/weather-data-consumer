FROM alpine:edge

RUN apk update
RUN apk add build-base make python3 py3-pip

COPY ./i4cast_consumer /srv/i4cast_consumer
COPY ./requirements.txt /srv/requirements.txt

RUN pip3 install -r /srv/requirements.txt --upgrade

WORKDIR /srv
ENV PYTHONPATH /srv

VOLUME [ "/srv/dist" ]