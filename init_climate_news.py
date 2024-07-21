import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.crud.climate_news import ClimateNewsCRUD
from app.db.base import Base
from app.models.climate_news import ClimateNews

# Database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create a new database session
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def erase_and_create_tables():
    # Drop the tables if they exist
    Base.metadata.drop_all(bind=engine, tables=[ClimateNews.__table__])
    # Create the tables
    Base.metadata.create_all(bind=engine, tables=[ClimateNews.__table__])

def main():
    erase_and_create_tables()

    db = next(get_db())
    file_path = "Sentometrics_US_Media_Climate_Change_Index.xlsx"

    # Populate the database with climate news data
    ClimateNewsCRUD.populate_climate_news(db, file_path)
    print("Database populated with climate news data.")

if __name__ == "__main__":
    main()
