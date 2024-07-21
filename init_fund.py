import random
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.crud.funds import FundCRUD
from app.crud.climate_fund import ClimateFundCRUD
from app.db.base import Base
from app.models.funds import Fund, Holding, FundReturn
from app.models.climate_fund import ClimateFund, ClimateHolding, ClimateFundReturn
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

db = next(get_db())
term = ""
country = "us"
page_size = 100
currency = "USD"
start_date = datetime(2020, 1, 1)
end_date = datetime(2023, 1, 1)



def erase_and_create_tables():
    # Drop the tables if they exist
    Base.metadata.drop_all(bind=engine, tables=[Fund.__table__, Holding.__table__, FundReturn.__table__])
    # Create the tables
    Base.metadata.create_all(bind=engine, tables=[Fund.__table__, Holding.__table__, FundReturn.__table__])
    Base.metadata.drop_all(bind=engine, tables=[ClimateFund.__table__, ClimateHolding.__table__, ClimateFundReturn.__table__])
    # Create the tables
    Base.metadata.create_all(bind=engine, tables=[ClimateFund.__table__, ClimateHolding.__table__, ClimateFundReturn.__table__])


erase_and_create_tables()

# Populate the database with funds, their holdings, and historical prices
FundCRUD.populate_funds(db, term, country, page_size, currency, start_date, end_date)
print("Database populated with funds, their holdings, and historical prices.")
climate_fund_share_class_ids = [
    "FOUSA00EQ9", "FOUSA00EOF", "FOUSA00JXN", "FOUSA02W00", "F000010I8X"
    # Add more climate-focused fundShareClassId values
]
start_date = datetime(2020, 1, 1)
end_date = datetime(2023, 1, 1)

# Populate the database with climate-focused funds, their holdings, and historical returns
ClimateFundCRUD.populate_climate_funds(db, climate_fund_share_class_ids, start_date, end_date)
print("Database populated with climate-focused funds, their holdings, and historical returns.")
