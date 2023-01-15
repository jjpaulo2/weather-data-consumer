import asyncio

from redis.asyncio import Redis


from i4cast_consumer.settings import ApiSettings, CacheSettings
from i4cast_consumer.talkers import I4castTalker


async def main():
    cache_settings = CacheSettings()
    api_settings = ApiSettings()

    redis = Redis(
        host=cache_settings.HOST,
        port=cache_settings.PORT
    )
    talker = I4castTalker(
        api_settings=api_settings,
        cache_settings=cache_settings,
        redis=redis
    )


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
