from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import models
import schemas
from datetime import datetime

# Mission CRUD
def get_mission(db: Session, mission_id: int):
    return db.query(models.Mission).filter(models.Mission.id == mission_id).first()

def get_mission_by_name(db: Session, name: str):
    return db.query(models.Mission).filter(models.Mission.name == name).first()

def get_missions(db: Session, skip: int = 0, limit: int = 100, status: str = None):
    query = db.query(models.Mission)
    if status:
        query = query.filter(models.Mission.status == status)
    return query.offset(skip).limit(limit).all()

def create_mission(db: Session, mission: schemas.MissionCreate):
    db_mission = models.Mission(**mission.model_dump())
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)
    return db_mission

def update_mission_status(db: Session, mission_id: int, status: str):
    mission = get_mission(db, mission_id)
    if mission:
        mission.status = status
        if status == "Completed":
            mission.end_date = datetime.utcnow()
        db.commit()
        db.refresh(mission)
    return mission

def delete_mission(db: Session, mission_id: int):
    mission = get_mission(db, mission_id)
    if mission:
        db.delete(mission)
        db.commit()
        return True
    return False

# Astronaut CRUD
def get_astronaut(db: Session, astronaut_id: int):
    return db.query(models.Astronaut).filter(models.Astronaut.id == astronaut_id).first()

def get_astronauts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Astronaut).offset(skip).limit(limit).all()

def create_astronaut(db: Session, astronaut: schemas.AstronautCreate):
    db_astronaut = models.Astronaut(**astronaut.model_dump())
    db.add(db_astronaut)
    db.commit()
    db.refresh(db_astronaut)
    return db_astronaut

def assign_astronaut_to_mission(db: Session, astronaut_id: int, mission_id: int):
    astronaut = get_astronaut(db, astronaut_id)
    mission = get_mission(db, mission_id)
    if astronaut and mission:
        astronaut.mission_id = mission_id
        db.commit()
        db.refresh(astronaut)
        return astronaut
    return None

# Rocket CRUD
def get_rocket(db: Session, rocket_id: int):
    return db.query(models.Rocket).filter(models.Rocket.id == rocket_id).first()

def get_rockets(db: Session, skip: int = 0, limit: int = 100, active_only: bool = False):
    query = db.query(models.Rocket)
    if active_only:
        query = query.filter(models.Rocket.active == True)
    return query.offset(skip).limit(limit).all()

def create_rocket(db: Session, rocket: schemas.RocketCreate):
    db_rocket = models.Rocket(**rocket.model_dump())
    db.add(db_rocket)
    db.commit()
    db.refresh(db_rocket)
    return db_rocket

def assign_rocket_to_mission(db: Session, rocket_id: int, mission_id: int):
    rocket = get_rocket(db, rocket_id)
    if rocket:
        rocket.mission_id = mission_id
        db.commit()
        db.refresh(rocket)
        return rocket
    return None
