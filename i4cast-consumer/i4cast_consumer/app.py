from asyncio import Runner
from uvloop import new_event_loop

from redis.asyncio import Redis
from mongoengine.connection import (
    connect as mongodb_connect
)

from i4cast_consumer.talkers import I4castTalker
from i4cast_consumer.settings import (
    I4castApiSettings,
    RedisSettings,
    RedisExtraSettings,
    MongoDbSettings,
    JsonExportingSettings
)
from i4cast_consumer.services import GetAndSaveEnvironmentalData


async def main() -> None:
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
    await service.run()


def run_main() -> None:
    with Runner(loop_factory=new_event_loop) as uv_runner:
        uv_runner.run(main())


if __name__ == '__main__':
    run_main()
