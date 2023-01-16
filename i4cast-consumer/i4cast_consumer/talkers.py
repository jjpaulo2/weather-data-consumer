from typing import Self, Optional
from httpx import AsyncClient, codes
from redis.asyncio import Redis

from i4cast_consumer.exceptions import (
    UnauthorizedException,
    NotFoundEnvironmentalDataException
)
from i4cast_consumer.models import EnvironmentalType
from i4cast_consumer.settings import (
    I4castApiSettings,
    RedisExtraSettings
)


class I4castTalker:

    def __init__(self, api_settings: I4castApiSettings, redis_settings: RedisExtraSettings, redis: Redis) -> Self:
        self._api_settings = api_settings
        self._redis_settings = redis_settings
        self._redis = redis

    @property
    def _auth_request_uri(self) -> str:
        return self._api_settings.host + self._api_settings.routes.auth

    @property
    def _stations_request_uri(self) -> str:
        return self._api_settings.host + self._api_settings.routes.stations

    @property
    def _environmental_data_request_uri(self) -> str:
        return self._api_settings.host + self._api_settings.routes.environmental_data

    @property
    def _auth_request_body(self) -> dict:
        return {
            'user': self._api_settings.username,
            'password': self._api_settings.password,
            'keep_connected': True
        }

    @property
    def _stations_request_body(self) -> dict:
        return {
            'region': self._api_settings.region
        }

    def _get_environmental_data_request_body(self, station_id: int, env_type: EnvironmentalType) -> dict:
        return {
            "station_id": station_id,
            "region": self._api_settings.region,
            "data_type": "forecast",
            "environmental_type": env_type.value
        }

    async def _get_auth_headers(self) -> dict[str, str]:
        return {
            'Authorization': f'Bearer {await self.get_auth_token()}'
        }

    async def _get_auth_token_from_api(self) -> str:
        response = None
        async with AsyncClient() as client:
            response = await client.post(
                self._auth_request_uri,
                json=self._auth_request_body
            )

        if response.status_code == codes.UNAUTHORIZED:
            raise UnauthorizedException()

        return response.json().get('access_token')

    async def _get_auth_token_from__redis(self) -> Optional[bytes]:
        return await self._redis.get(
            name=self._redis_settings.auth_token_key
        )

    async def _set_auth_token_to_redis(self, value: str) -> None:
        await self._redis.set(
            name=self._redis_settings.auth_token_key,
            value=value,
            ex=self._api_settings.auth_expiration
        )

    async def get_auth_token(self) -> str:
        cached_token = await self._get_auth_token_from__redis()

        if cached_token:
            return cached_token.decode(
                encoding=self._redis_settings.encoding
            )

        token_from_api = await self._get_auth_token_from_api()
        await self._set_auth_token_to_redis(token_from_api)

        return token_from_api

    async def get_stations(self) -> list[dict]:
        response = None
        async with AsyncClient() as client:
            response = await client.post(
                self._stations_request_uri,
                json=self._stations_request_body,
                headers=await self._get_auth_headers()
            )
        return response.json()

    async def get_environmental_data(self, station_id: int, environmental_type: EnvironmentalType) -> dict:
        response = None
        async with AsyncClient() as client:
            response = await client.post(
                self._environmental_data_request_uri,
                json=self._get_environmental_data_request_body(
                    station_id,
                    environmental_type
                ),
                headers=await self._get_auth_headers()
            )
        
        if response.status_code == codes.NOT_FOUND:
            raise NotFoundEnvironmentalDataException(
                station_id=station_id,
                env_type=environmental_type.value
            )

        return response.json()
