from pydantic import BaseSettings, Field


class I4castApiRoutes(BaseSettings):
    auth = '/v1/auth/login'
    stations = '/v1/atmocean/getStations'
    environmental_data = '/v1/atmocean/getEnvironmentalData'


class I4castApiSettings(BaseSettings):
    host: str = Field(env='I4CAST_HOST', default='http://0.0.0.0') #nosec
    username: str = Field(env='I4CAST_USERNAME')
    password: str = Field(env='I4CAST_PASSWORD')
    auth_expiration: int = Field(env='I4CAST_AUTH_EXPIRATION', default=300)
    region: str = Field(env='I4CAST_REGION', default='1711')
    routes = I4castApiRoutes()


class RedisSettings(BaseSettings):
    db: str = Field(env='REDIS_DB', default='0')
    host: str = Field(env='REDIS_HOST', default='0.0.0.0') # nosec
    port: str = Field(env='REDIS_PORT', default='6379')
    password: str = Field(env='REDIS_PASSWORD', default='')


class RedisExtraSettings(BaseSettings):
    encoding: str = Field(env='REDIS_ENCODING', default='utf-8')
    auth_token_key = 'i4cast_token' #nosec


class MongoDbSettings(BaseSettings):
    db: str = Field(env='MONGODB_DB', default='i4cast_data')
    host: str = Field(env='MONGODB_HOST', default='0.0.0.0') # nosec
    port: int = Field(env='MONGODB_PORT', default=27017)
    username: str = Field(env='MONGODB_USERNAME', default='admin')
    password: str = Field(env='MONGODB_PASSWORD', default='admin')


class JsonExportingSettings(BaseSettings):
    directory: str = Field(env='JSON_EXPORTING_DIRECTORY', default='dist')
