from json import dumps
from datetime import datetime
from os import makedirs
from contextlib import suppress

from i4cast_consumer.settings import JsonExportingSettings
from i4cast_consumer.models import EnvironmentalDataList


async def export_to_mongodb(environmental_data: dict) -> None:
    env_data_obj = EnvironmentalDataList(**environmental_data)
    env_data_obj.save()


async def export_to_json(environmental_data: dict, json_settings: JsonExportingSettings) -> None:
    with suppress(FileExistsError):
        makedirs(json_settings.directory)
    
    filename = '{dir}/environmental-data-{station_id}-{env_type}-{now}.json'.format(
        dir=json_settings.directory,
        station_id=environmental_data.get('station_id'),
        env_type=environmental_data.get('environmental_type'),
        now=datetime.now().isoformat()
    )
    with open(filename, mode='w', encoding='utf-8') as json_data:
        json_data.write(
            dumps(environmental_data)
        )
    