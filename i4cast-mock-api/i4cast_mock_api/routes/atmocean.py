from json import JSONDecodeError, loads
from pathlib import Path

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from i4cast_mock_api.schemas.atmocean import (
    GetStationsSchema,
    GetEnvironmentalDataSchema
)


current_dir = Path(__file__).parent
router = APIRouter(
    tags=['AtmoceanController'],
    prefix='/v1/atmocean'
)


@router.post('/getStations')
def stations(_: GetStationsSchema) -> JSONResponse:
    try:
        with open(f'{current_dir}/responses/getStations.json') as stations_json:
            return JSONResponse(
                content=loads(stations_json.read()),
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


@router.post('/getEnvironmentalData')
def environmental_data(_: GetEnvironmentalDataSchema) -> JSONResponse:
    try:
        with open(f'{current_dir}/responses/getEnvironmentalData.json') as environmental_data_json:
            return JSONResponse(
                content=loads(environmental_data_json.read()),
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
