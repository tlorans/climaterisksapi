from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.crud.climate_signal import ClimateSignalCRUD
from app.db.base import Base
from app.models.climate_fund import ClimateFund, ClimateFundReturn
from app.models.climate_news import ClimateNews
from app.models.climate_signal import ClimateSignal

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
    Base.metadata.drop_all(bind=engine, tables=[ClimateSignal.__table__])
    # Create the tables
    Base.metadata.create_all(bind=engine, tables=[ClimateSignal.__table__])



def main():
    erase_and_create_tables()

    db = next(get_db())

    climate_news_name = "aggregate"  # Update this to the desired climate news series name

    # Generate and save the climate factor signal
    ClimateSignalCRUD.generate_climate_factor_signal(db, climate_news_name)

if __name__ == "__main__":
    main()
