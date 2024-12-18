from typing import List, Optional

from pydantic import BaseModel

class AddressDTO(BaseModel):
    region: Optional[str]
    city: str
    district: Optional[str]
    street: Optional[str]
    house: Optional[str]
    location: str

class AddressRequest(BaseModel):
    id: int

class AddressResult(BaseModel):
   id: int

class Geometry(BaseModel):
    type: str
    coordinates: List[float]

class AddressProperties(BaseModel):
    city: str
    region: Optional[str]
    street: Optional[str]
    district: Optional[str]
    house: Optional[str]

class GeoJson(BaseModel):
    type: str
    geometry: Geometry
    properties: AddressProperties