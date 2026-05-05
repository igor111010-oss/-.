from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import crud
import schemas
from database import get_db

router = APIRouter(prefix="/api/missions", tags=["missions"])

@router.post("/", response_model=schemas.Mission)
def create_mission(mission: schemas.MissionCreate, db: Session = Depends(get_db)):
    existing = crud.get_mission_by_name(db, mission.name)
    if existing:
        raise HTTPException(status_code=400, detail="Mission already exists")
    return crud.create_mission(db, mission)

@router.get("/", response_model=List[schemas.Mission])
def read_missions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    missions = crud.get_missions(db, skip=skip, limit=limit, status=status)
    return missions

@router.get("/{mission_id}", response_model=schemas.MissionDetail)
def read_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = crud.get_mission(db, mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@router.patch("/{mission_id}/status")
def update_mission_status(mission_id: int, status: str, db: Session = Depends(get_db)):
    mission = crud.update_mission_status(db, mission_id, status)
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return {"message": "Status updated", "mission": mission}

@router.delete("/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    if crud.delete_mission(db, mission_id):
        return {"message": "Mission deleted"}
    raise HTTPException(status_code=404, detail="Mission not found")
