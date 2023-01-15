from mongoengine.connection import connect
from redis.asyncio import Redis

# from i4cast_consumer.models import (
#     Station,
#     EnvironmentalDataList
# )

from i4cast_consumer.talker import I4castTalker


if __name__ == '__main__':
    # connect()
    redis = Redis()
    talker = I4castTalker()