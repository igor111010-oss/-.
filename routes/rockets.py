from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import crud
import schemas
from database import get_db

router = APIRouter(prefix="/api/rockets", tags=["rockets"])

@router.post("/", response_model=schemas.Rocket)
def create_rocket(rocket: schemas.RocketCreate, db: Session = Depends(get_db)):
    return crud.create_rocket(db, rocket)

@router.get("/", response_model=List[schemas.Rocket])
def read_rockets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    active_only: Optional[bool] = False,
    db: Session = Depends(get_db)
):
    rockets = crud.get_rockets(db, skip=skip, limit=limit, active_only=active_only)
    return rockets

@router.get("/{rocket_id}", response_model=schemas.Rocket)
def read_rocket(rocket_id: int, db: Session = Depends(get_db)):
    rocket = crud.get_rocket(db, rocket_id)
    if rocket is None:
        raise HTTPException(status_code=404, detail="Rocket not found")
    return rocket

@router.post("/{rocket_id}/assign/{mission_id}")
def assign_rocket(rocket_id: int, mission_id: int, db: Session = Depends(get_db)):
    result = crud.assign_rocket_to_mission(db, rocket_id, mission_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Rocket or Mission not found")
    return {"message": "Rocket assigned to mission"}
