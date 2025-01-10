from typing import List, Optional

from pydantic import BaseModel, Field


class AddressDTO(BaseModel):
    region: Optional[str]
    city: str
    district: Optional[str]
    street: Optional[str]
    house: Optional[str]
    location: str


class Geometry(BaseModel):
    type: str = Field("Point")
    coordinates: List[float]

class AddressProperties(BaseModel):
    city: str
    region: Optional[str]
    street: Optional[str]
    district: Optional[str] = Field(None)
    house: Optional[str]

class GeoJson(BaseModel):
    type: str = Field("Feature")
    geometry: Geometry
    properties: AddressProperties