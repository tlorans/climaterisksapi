from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.schemas.universe import UniverseCreate, Universe
from app.crud.universe import UniverseCRUD
from app.dependencies import get_db

router = APIRouter()

@router.post("/universes/", response_model=Universe)
def create_universe(universe: UniverseCreate, db: Session = Depends(get_db)):
    return UniverseCRUD.create_universe(db=db, universe=universe)

@router.get("/universes/{name}/{month}", response_model=Universe)
def read_universe(name: str, month: date, db: Session = Depends(get_db)):
    db_universe = UniverseCRUD.get_universe(db, name=name, month=month)
    if db_universe is None:
        raise HTTPException(status_code=404, detail="Universe not found")
    return db_universe

@router.get("/universes/", response_model=List[Universe])
def read_universes(month: date, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    universes = UniverseCRUD.get_universes(db, month=month, skip=skip, limit=limit)
    return universes

@router.get("/universes/dates/", response_model=List[date])
def read_universe_dates(db: Session = Depends(get_db)):
    universe_dates = UniverseCRUD.get_dates(db)
    if not universe_dates:
        raise HTTPException(status_code=404, detail="No dates found")
    return [record[0] for record in universe_dates]
