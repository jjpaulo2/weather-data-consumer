from asyncio import Runner
from typing import Optional
from uvloop import new_event_loop

from redis.asyncio import Redis
from mongoengine.connection import (
    connect as mongodb_connect
)

from i4cast_consumer.models import EnvironmentalType
from i4cast_consumer.talkers import I4castTalker
from i4cast_consumer.settings import (
    I4castApiSettings,
    RedisSettings,
    RedisExtraSettings,
    MongoDbSettings,
    JsonExportingSettings
)
from i4cast_consumer.services import GetAndSaveEnvironmentalData


async def main(station_id: Optional[int] = None, env_type: Optional[EnvironmentalType] = None) -> None:
    mongodb_connect(**MongoDbSettings().dict())
    redis = Redis(**RedisSettings().dict())
    talker = I4castTalker(
        api_settings=I4castApiSettings(),
        redis_settings=RedisExtraSettings(),
        redis=redis
    )
    service = GetAndSaveEnvironmentalData(
        api_talker=talker,
        json_settings=JsonExportingSettings()
    )
    await service.run(station_id, env_type)


def run_main(station_id: Optional[int] = None, env_type: Optional[EnvironmentalType] = None) -> None:
    with Runner(loop_factory=new_event_loop) as uv_runner:
        uv_runner.run(
            main(station_id, env_type)
        )


if __name__ == '__main__':
    run_main()
