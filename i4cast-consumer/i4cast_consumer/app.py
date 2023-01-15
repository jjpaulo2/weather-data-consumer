import asyncio

from redis.asyncio import Redis
from mongoengine.connection import (
    connect as mongodb_connect
)

from i4cast_consumer.models import (
    EnvironmentalType,
    EnvironmentalDataList
)
from i4cast_consumer.settings import (
    I4castApiSettings,
    RedisSettings,
    RedisExtraSettings,
    MongoDbSettings
)
from i4cast_consumer.talkers import I4castTalker


async def main():
    mongodb_connect(**MongoDbSettings().dict())
    redis = Redis(**RedisSettings().dict())
    talker = I4castTalker(
        api_settings=I4castApiSettings(),
        redis_settings=RedisExtraSettings(),
        redis=redis
    )

    for station in await talker.get_stations():
        for env_type in EnvironmentalType:
            env_data = await talker.get_environmental_data(
                station_id=station.get('station_id'),
                environmental_type=env_type
            )
            env_data_obj = EnvironmentalDataList(**env_data)
            env_data_obj.save()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
