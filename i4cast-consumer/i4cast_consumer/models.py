from mongoengine.document import (
    Document,
    EmbeddedDocument
)
from mongoengine.fields import (
    StringField,
    FloatField,
    IntField,
    DateTimeField,
    ReferenceField,
    EmbeddedDocumentListField
)


class Station(Document):
    station_id = IntField()
    station_name = StringField()
    station_depth = FloatField()
    station_depth_unit = StringField()
    station_lat = FloatField()
    station_lon = FloatField()


class EnvironmentalData(EmbeddedDocument):
    date = DateTimeField()
    environmental_variable = StringField()
    value = FloatField()
    units = StringField()


class EnvironmentalDataList(Document):
    station = ReferenceField(Station)
    macro_region = StringField()
    region = StringField()
    region_timezone = StringField()
    data_type = StringField()
    environmental_type = StringField()
    environmental_data = EmbeddedDocumentListField(
        EnvironmentalData
    )
