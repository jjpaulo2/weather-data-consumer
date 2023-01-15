from pydantic import BaseSettings, Field


class ApiSettings(BaseSettings):
    HOST: str = Field(env='I4CAST_HOST', default='http://0.0.0.0') #nosec
    USERNAME: str = Field(env='I4CAST_USERNAME')
    PASSWORD: str = Field(env='I4CAST_PASSWORD')
    AUTH_EXPIRATION: int = Field(env='I4CAST_AUTH_EXPIRATION', default=300)
    REGION: str = Field(env='I4CAST_REGION', default='1711')

    AUTH_URL = '/v1/auth/login'
    STATIONS_URL = '/v1/atmocean/getStations'
    ENVIRONMENTAL_DATA_URL = '/v1/atmocean/getEnvironmentalData'
    
class CacheSettings(BaseSettings):
    HOST: str = Field(env='REDIS_HOST', default='0.0.0.0') # nosec
    PORT: str = Field(env='REDIS_PORT', default='6379')
    ENCODING: str = Field(env='REDIS_ENCODING', default='utf-8')
    AUTH_TOKEN_KEY = 'i4cast_token' #nosec
