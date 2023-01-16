from typing import Optional, Self
from sys import exit

from i4cast_consumer.exceptions import (
    NotFoundEnvironmentalDataException,
    UnauthorizedException
)
from i4cast_consumer.settings import JsonExportingSettings
from i4cast_consumer.models import EnvironmentalType
from i4cast_consumer.talkers import I4castTalker
from i4cast_consumer.exporters import (
    export_to_json,
    export_to_mongodb
)


class GetAndSaveEnvironmentalData:

    def __init__(self, api_talker: I4castTalker, json_settings: JsonExportingSettings) -> Self:
        self._api_talker = api_talker
        self._json_settings = json_settings

    async def _export_data(self, env_data: dict) -> None:
        await export_to_mongodb(env_data)
        await export_to_json(env_data, self._json_settings)

    async def _consume_data(self, station_id: int, env_type: EnvironmentalType) -> None:
        env_data = await self._api_talker.get_environmental_data(
            station_id=station_id,
            environmental_type=env_type
        )
        print(
            'Dados encontrados para os parâmetros fornecidos.',
            f'station_id: \'{station_id}\'.',
            f'env_type: \'{env_type.value}\'.'
        )
        await self._export_data(env_data)

    async def _consume_complete_data(self) -> None:
        for station in await self._api_talker.get_stations():
            for env_type in EnvironmentalType:
                await self._consume_data(
                    station_id=station.get('station_id', 0),
                    env_type=env_type
                )

    async def run(self, station_id: Optional[int] = None, env_type: Optional[EnvironmentalType] = None) -> None:
        try:
            if station_id and env_type:
                await self._consume_data(station_id, env_type)
            else:
                await self._consume_complete_data()

        except NotFoundEnvironmentalDataException as exc:
            print(
                exc.message,
                f'station_id: \'{exc.station_id}\'.',
                f'env_type: \'{exc.env_type}\'.'
            )
            exit(-1)

        except UnauthorizedException as exc:
            print(exc.message)
            exit(-1)
