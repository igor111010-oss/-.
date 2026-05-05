from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Mission(Base):
    __tablename__ = "missions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    agency = Column(String)
    launch_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    status = Column(String)  # Planning, Active, Completed, Failed
    description = Column(Text)
    destination = Column(String)  # ISS, Moon, Mars, Orbit, etc.
    
    astronauts = relationship("Astronaut", back_populates="mission")
    rockets = relationship("Rocket", back_populates="mission")

class Astronaut(Base):
    __tablename__ = "astronauts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    nationality = Column(String)
    age = Column(Integer)
    experience_years = Column(Float)
    status = Column(String)  # Active, Retired, In Training
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=True)
    
    mission = relationship("Mission", back_populates="astronauts")

class Rocket(Base):
    __tablename__ = "rockets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    manufacturer = Column(String)
    height_meters = Column(Float)
    diameter_meters = Column(Float)
    mass_kg = Column(Float)
    payload_to_leo_kg = Column(Float)
    first_flight = Column(DateTime)
    active = Column(Boolean, default=True)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=True)
    
    mission = relationship("Mission", back_populates="rockets")
