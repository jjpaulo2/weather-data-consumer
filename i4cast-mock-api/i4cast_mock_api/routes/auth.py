from json import JSONDecodeError, loads
from pathlib import Path

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from i4cast_mock_api.schemas.auth import AuthLoginSchema


current_dir = Path(__file__).parent
router = APIRouter(
    tags=['AuthController'],
    prefix='/v1/auth'
)


@router.post('/login')
def login(_: AuthLoginSchema) -> JSONResponse:
    try:
        with open(f'{current_dir}/responses/login.json') as login_json:
            return JSONResponse(
                content=loads(login_json.read()),
                status_code=status.HTTP_200_OK
            )
            
    except (JSONDecodeError, FileNotFoundError) as exc:
        return JSONResponse(
            content={
                'message': 'You got an error!',
                'detail': str(exc)
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
