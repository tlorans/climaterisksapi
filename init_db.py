import os
import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.universe import Universe, Stock
from app.schemas.universe import UniverseCreate, StockCreate
from app.crud.universe import UniverseCRUD
from app.db.base import Base

from app.models.returns import StockReturn
from app.crud.returns import StockReturnCRUD

# Database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create a new database session
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db = next(get_db())

# erase previous table if it exists
# Drop the Universe and Stock tables if they exist
Base.metadata.drop_all(bind=engine, tables=[Universe.__tablename__, Stock.__tablename__])
print(f"Tables dropped: {Universe.__tablename__, Stock.__tablename__}")
# Create the Universe and Stock tables
Base.metadata.create_all(bind=engine, tables=[Universe.__tablename__, Stock.__tablename__])
print(f"Tables created: {Universe.__tablename__, Stock.__tablename__}")

UniverseCRUD.create_random_universes(db)

# erase previous table if it exists
# Drop the Universe and Stock tables if they exist
Base.metadata.drop_all(bind=engine, tables=[StockReturn.__tablename__])
print(f"Tables dropped: {StockReturn.__tablename__}")
# Create the Universe and Stock tables
Base.metadata.create_all(bind=engine, tables=[StockReturn.__tablename__])
print(f"Tables created: {StockReturn.__tablename__}")


StockReturnCRUD.populate_stock_returns(db)