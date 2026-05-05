from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MissionBase(BaseModel):
    name: str
    agency: str
    launch_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str
    description: str
    destination: str

class MissionCreate(MissionBase):
    pass

class Mission(MissionBase):
    id: int
    class Config:
        from_attributes = True

class AstronautBase(BaseModel):
    name: str
    nationality: str
    age: int
    experience_years: float
    status: str
    mission_id: Optional[int] = None

class AstronautCreate(AstronautBase):
    pass

class Astronaut(AstronautBase):
    id: int
    class Config:
        from_attributes = True

class RocketBase(BaseModel):
    name: str
    manufacturer: str
    height_meters: float
    diameter_meters: float
    mass_kg: float
    payload_to_leo_kg: float
    first_flight: Optional[datetime] = None
    active: bool = True
    mission_id: Optional[int] = None

class RocketCreate(RocketBase):
    pass

class Rocket(RocketBase):
    id: int
    class Config:
        from_attributes = True

class MissionDetail(Mission):
    astronauts: List[Astronaut] = []
    rockets: List[Rocket] = []
