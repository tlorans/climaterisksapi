from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.universe import UniverseCreate, Universe
from app.crud import universe
from app.dependencies import get_db
from typing import List

router = APIRouter()

@router.post("/universes/", response_model=Universe)
def create_universe(universe: UniverseCreate, db: Session = Depends(get_db)):
    return universe.create_universe(db=db, universe=universe)

@router.get("/universes/{universe_id}", response_model=Universe)
def read_universe(universe_id: int, db: Session = Depends(get_db)):
    db_universe = universe.get_universe(db, universe_id=universe_id)
    if db_universe is None:
        raise HTTPException(status_code=404, detail="Universe not found")
    return db_universe

@router.get("/universes/", response_model=List[Universe])
def read_universes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    universes = universe.get_universes(db, skip=skip, limit=limit)
    return universes
