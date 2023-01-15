from pydantic import BaseSettings, Field


class ApiSettings(BaseSettings):
    HOST: str = Field(env='I4CAST_HOST', default='http://0.0.0.0')
    USERNAME: str = Field(env='I4CAST_USERNAME')
    PASSWORD: str = Field(env='I4CAST_PASSWORD')
    AUTH_DURATION: int = Field(env='I4CAST_AUTH_DURATION', default=300)
    REGION: str = Field(env='I4CAST_REGION', default='1711')

    AUTH_URL = '/v1/auth/login'
    STATIONS_URL = '/v1/atmocean/getStations'
    ENVIRONMENTAL_DATA_URL = '/v1/atmocean/getEnvironmentalData'
    