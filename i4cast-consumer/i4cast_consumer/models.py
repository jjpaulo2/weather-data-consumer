from enum import Enum

from mongoengine.document import (
    Document,
    EmbeddedDocument
)
from mongoengine.fields import (
    StringField,
    FloatField,
    IntField,
    EmbeddedDocumentListField
)


class EnvironmentalType(Enum):
    WEATHER = 'weather'
    WATER_FLOW = 'water_flow'
    WAVE = 'wave'

    @classmethod
    def list(cls) -> list[str]:
        return [item.value for item in cls]


class EnvironmentalData(EmbeddedDocument):
    date = StringField()
    environmental_variable = StringField()
    value = FloatField()
    units = StringField()


class EnvironmentalDataList(Document):
    station_id = IntField()
    station_name = StringField()
    station_depth = FloatField()
    station_depth_unit = StringField()
    station_lat = FloatField()
    station_lon = FloatField()
    macro_region = StringField()
    region = StringField()
    region_timezone = StringField()
    data_type = StringField()
    environmental_type = StringField(
        choices=EnvironmentalType.list()
    )
    environmental_data = EmbeddedDocumentListField(
        EnvironmentalData
    )
