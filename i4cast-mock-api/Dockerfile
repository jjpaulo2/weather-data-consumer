FROM alpine:edge

RUN apk update
RUN apk add build-base make python3 py3-pip

COPY ./i4cast_mock_api /srv/i4cast_mock_api
COPY ./requirements.txt /srv/requirements.txt
COPY ./gunicorn.conf.py /srv/gunicorn.conf.py
COPY ./run.sh /srv/run.sh

RUN pip3 install -r /srv/requirements.txt --upgrade

WORKDIR /srv

ENV APP_PORT 8880
ENV PYTHONPATH /srv

EXPOSE 8880

ENTRYPOINT [ "sh", "run.sh" ]