from typing import Self
from redis.asyncio import Redis

from i4cast_consumer.models import EnvironmentalType
from i4cast_consumer.settings import ApiSettings


class I4castTalker:

    def __init__(self, api_settings: ApiSettings, redis: Redis) -> Self:
        self.auth_duration = api_settings.AUTH_DURATION
        self.username = api_settings.USERNAME
        self.password = api_settings.PASSWORD
        self.region = api_settings.REGION
        self.redis = redis

    async def get_auth_token(self) -> str:
        pass

    async def get_stations(self) -> list[dict]:
        pass

    async def get_environmental_data(self, station_id: int, environmental_type: EnvironmentalType) -> dict:
        pass
