FROM python:3.11-alpine

RUN apk update
RUN apk add build-base make

COPY ./i4cast_consumer /srv/i4cast_consumer
COPY ./requirements.txt /srv/requirements.txt
COPY ./job.sh /srv/job.sh

RUN pip3 install -r /srv/requirements.txt --upgrade

WORKDIR /srv

ENV PYTHONPATH '/srv'
ENV JSON_EXPORTING_DIRECTORY '/srv/dist'
ENV I4CAST_JOB_STATION '27'
ENV I4CAST_JOB_ENVIRONMENTAL_TYPE 'weather'
ENV CRON_EXPRESSION '* * * * *'
ENV CRON_COMMAND 'sh /srv/job.sh $I4CAST_JOB_STATION $I4CAST_JOB_ENVIRONMENTAL_TYPE'

RUN echo "$CRON_EXPRESSION $CRON_COMMAND" >> /var/spool/cron/crontabs/root

VOLUME [ "/srv/dist" ]

ENTRYPOINT [ "crond", "-f" ]