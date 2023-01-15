from typing import Self
from httpx import AsyncClient
from redis.asyncio import Redis

# from i4cast_consumer.models import EnvironmentalType
from i4cast_consumer.settings import ApiSettings


class I4castTalker:

    def __init__(self, settings: ApiSettings, redis: Redis) -> Self:
        self.settings = settings
        self.redis = redis

    @property
    def auth_request_uri(self) -> str:
        return self.settings.HOST + self.settings.AUTH_URL

    @property
    def auth_request_body(self) -> dict:
        return {
            'username': self.settings.USERNAME,
            'password': self.settings.PASSWORD,
            'keep_connected': True
        }

    async def get_auth_token(self) -> str:
        response = None
        async with AsyncClient() as client:
            response = await client.post(
                self.auth_request_uri,
                json=self.auth_request_body
            )
        return response.json().get('access_token')

    # async def get_stations(self) -> list[dict]:
    #     pass

    # async def get_environmental_data(self, station_id: int, environmental_type: EnvironmentalType) -> dict:
    #     pass
