from functools import lru_cache
from i4cast_mock_api.settings import AppSettings


@lru_cache
def app_settings() -> AppSettings:
    return AppSettings()
