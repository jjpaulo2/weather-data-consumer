from pydantic import BaseSettings, Field


class ApiSettings(BaseSettings):
    USERNAME: str = Field(env='I4CAST_USERNAME')
    PASSWORD: str = Field(env='I4CAST_PASSWORD')
    AUTH_DURATION: int = Field(env='I4CAST_AUTH_DURATION', default=300)
    REGION: str = Field(env='I4CAST_REGION', default='1711')
