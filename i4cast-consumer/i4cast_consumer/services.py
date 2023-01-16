from typing import Self

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

    async def run(self) -> None:
        for station in await self._api_talker.get_stations():
            for env_type in EnvironmentalType:
                env_data = await self._api_talker.get_environmental_data(
                    station_id=station.get('station_id'),
                    environmental_type=env_type
                )
                if env_data.get('status') != 404:
                    await self._export_data(env_data)
