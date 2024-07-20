from sqlalchemy.orm import Session
from app.schemas.universe import Universe, Stock
from app.schemas.universe import UniverseCreate

def create_universe(db: Session, universe: UniverseCreate):
    db_universe = Universe(
        name=universe.name,
        month=universe.month,
        stocks=[Stock(**stock.dict()) for stock in universe.stocks]
    )
    db.add(db_universe)
    db.commit()
    db.refresh(db_universe)
    return db_universe

def get_universe(db: Session, universe_id: int):
    return db.query(Universe).filter(Universe.id == universe_id).first()

def get_universes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Universe).offset(skip).limit(limit).all()
