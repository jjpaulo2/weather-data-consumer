from fastapi import FastAPI, APIRouter
from starlette.routing import BaseRoute

from i4cast_mock_api.dependencies import app_settings
from i4cast_mock_api import (
    __author__,
    __original_api__,
    __description__,
    __title__,
    __version__
)
from i4cast_mock_api.routes.auth import (
    router as auth_router
)
from i4cast_mock_api.routes.atmocean import (
    router as atmocean_router
)


def routes() -> list[BaseRoute]:
    root_router = APIRouter()
    root_router.include_router(auth_router)
    root_router.include_router(atmocean_router)
    return root_router.routes


def create_app() -> FastAPI:
    return FastAPI(
        title=__title__,
        description=__description__,
        version=__version__,
        docs_url='/v1/i4cast-api',
        openapi_url='/v1/openapi.json',
        routes=routes(),
        swagger_ui_parameters=app_settings().SWAGGER_PARAMS
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "app:create_app",
        host=app_settings().HOST,
        port=app_settings().PORT,
        reload=True
    )
