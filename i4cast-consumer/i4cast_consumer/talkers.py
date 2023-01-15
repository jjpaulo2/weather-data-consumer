from typing import Self, Optional
from httpx import AsyncClient
from redis.asyncio import Redis

from i4cast_consumer.models import EnvironmentalType
from i4cast_consumer.settings import ApiSettings, CacheSettings


class I4castTalker:

    def __init__(self, api_settings: ApiSettings, cache_settings: CacheSettings, redis: Redis) -> Self:
        self._api_settings = api_settings
        self._cache_settings = cache_settings
        self._redis = redis

    @property
    def _auth_request_uri(self) -> str:
        return self._api_settings.HOST + self._api_settings.AUTH_URL

    @property
    def _stations_request_uri(self) -> str:
        return self._api_settings.HOST + self._api_settings.STATIONS_URL

    @property
    def _environmental_data_request_uri(self) -> str:
        return self._api_settings.HOST + self._api_settings.ENVIRONMENTAL_DATA_URL

    @property
    def _auth_request_body(self) -> dict:
        return {
            'user': self._api_settings.USERNAME,
            'password': self._api_settings.PASSWORD,
            'keep_connected': True
        }

    @property
    def _stations_request_body(self) -> dict:
        return {
            'region': self._api_settings.REGION
        }

    def _get_environmental_data_request_body(self, station_id: int, env_type: EnvironmentalType) -> dict:
        return {
            "station_id": station_id,
            "region": self._api_settings.REGION,
            "data_type": "forecast",
            "environmental_type": env_type.value
        }

    async def _get_auth_headers(self) -> dict[str, str]:
        return {
            'Authentication': f'Bearer {await self.get_auth_token()}'
        }

    async def _get_auth_token_from_api(self) -> str:
        response = None
        async with AsyncClient() as client:
            response = await client.post(
                self._auth_request_uri,
                json=self._auth_request_body
            )
        return response.json().get('access_token')

    async def _get_auth_token_from__redis(self) -> Optional[bytes]:
        return await self._redis.get(
            name=self._cache_settings.AUTH_TOKEN_KEY
        )

    async def _set_auth_token_to__redis(self, value: str) -> None:
        await self._redis.set(
            name=self._cache_settings.AUTH_TOKEN_KEY,
            value=value,
            ex=self._api_settings.AUTH_EXPIRATION
        )

    async def get_auth_token(self) -> str:
        cached_token = await self._get_auth_token_from__redis()

        if cached_token:
            return cached_token.decode(
                encoding=self._cache_settings.ENCODING
            )

        token_from_api = await self._get_auth_token_from_api()
        await self._set_auth_token_to__redis(token_from_api)

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
        return response.json()
