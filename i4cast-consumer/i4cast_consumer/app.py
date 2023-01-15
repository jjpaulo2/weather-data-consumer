from mongoengine.connection import connect

from i4cast_consumer.models import (
    Station,
    EnvironmentalDataList
)

if __name__ == '__main__':
    connect()
    pass