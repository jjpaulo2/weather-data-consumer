from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    HOST: str = Field(env='APP_HOST', default='0.0.0.0') # nosec
    PORT: int = Field(env='APP_PORT', default=8880)
    SWAGGER_PARAMS = {
        "defaultModelsExpandDepth": -1
    }

    def host_binding(self) -> str:
        return f'{self.HOST}:{self.PORT}'
