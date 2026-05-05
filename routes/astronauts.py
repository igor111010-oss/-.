from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from database import get_db

router = APIRouter(prefix="/api/astronauts", tags=["astronauts"])

@router.post("/", response_model=schemas.Astronaut)
def create_astronaut(astronaut: schemas.AstronautCreate, db: Session = Depends(get_db)):
    return crud.create_astronaut(db, astronaut)

@router.get("/", response_model=List[schemas.Astronaut])
def read_astronauts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    astronauts = crud.get_astronauts(db, skip=skip, limit=limit)
    return astronauts

@router.get("/{astronaut_id}", response_model=schemas.Astronaut)
def read_astronaut(astronaut_id: int, db: Session = Depends(get_db)):
    astronaut = crud.get_astronaut(db, astronaut_id)
    if astronaut is None:
        raise HTTPException(status_code=404, detail="Astronaut not found")
    return astronaut

@router.post("/{astronaut_id}/assign/{mission_id}")
def assign_astronaut(astronaut_id: int, mission_id: int, db: Session = Depends(get_db)):
    result = crud.assign_astronaut_to_mission(db, astronaut_id, mission_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Astronaut or Mission not found")
    return {"message": "Astronaut assigned to mission"}
