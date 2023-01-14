from pydantic import BaseModel


class GetStationsSchema(BaseModel):
    region: str
    

class GetEnvironmentalDataSchema(BaseModel):
    station_id: int
    region: str
    data_type: str
    environmental_type: str
    