from sqlalchemy.orm import Session
from app.models.universe import Universe, Stock
from app.schemas.universe import UniverseCreate
from datetime import date
import random
import pandas as pd

class UniverseCRUD:
    zones = ["Zone A", "Zone B", "Zone C", "Zone D"]
    zone_mapping = {
        "Zone A": ["Zone A"],
        "Zone B": ["Zone B"],
        "Zone C": ["Zone C"],
        "Zone D": ["Zone D"],
        "Zone E": ["Zone A", "Zone B"],
        "Zone F": ["Zone C", "Zone D"],
    }

    all_stocks = {f"STOCK{i:04d}": {"ticker": f"STOCK{i:04d}", "name": f"Stock {i}"} for i in range(1, 1001)}
    stock_assignment = {zone: [] for zone in zones}

    # Define date range for monthly returns
    date_range = pd.date_range(start='2020-01-01', end='2023-01-01', freq='ME')

    @staticmethod
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

    @staticmethod
    def get_universe(db: Session, name: str, month: date):
        return db.query(Universe).filter(Universe.name == name, Universe.month == month).first()

    @staticmethod
    def get_universes(db: Session, month: date, skip: int = 0, limit: int = 10):
        return db.query(Universe).filter(Universe.month == month).offset(skip).limit(limit).all()

    @staticmethod
    def get_dates(db: Session):
        return db.query(Universe.month).distinct().all()

    @staticmethod
    def create_random_universe_for_month(db: Session, month: date):
        stocks = UniverseCRUD.stock_assignment

        # Assign stocks to base zones (A, B, C, D)
        for zone in UniverseCRUD.zones:
            # Ensure each stock only appears in one zone
            remaining_stocks = list(set(UniverseCRUD.all_stocks.keys()) - set(sum(stocks.values(), [])))
            while len(stocks[zone]) < 100 and remaining_stocks:
                stock = random.choice(remaining_stocks)
                remaining_stocks.remove(stock)
                stocks[zone].append(stock)

            # Randomly remove some stocks to simulate disappearance (10% chance)
            stocks[zone] = [stock for stock in stocks[zone] if random.random() > 0.1]

        # Randomly add some new stocks to simulate appearance (10 new stocks)
        for _ in range(10):
            remaining_stocks = list(set(UniverseCRUD.all_stocks.keys()) - set(sum(stocks.values(), [])))
            if not remaining_stocks:
                break
            stock = random.choice(remaining_stocks)
            zone = random.choice(UniverseCRUD.zones)
            stocks[zone].append(stock)

        # Create combined zones based on the mapping
        for combined_zone, base_zones in UniverseCRUD.zone_mapping.items():
            combined_stocks = []
            for base_zone in base_zones:
                combined_stocks.extend(stocks[base_zone])
            stocks[combined_zone] = combined_stocks

        # Create and save universes for each zone for the current month
        for zone, stock_list in stocks.items():
            universe_stocks = []
            for ticker in stock_list:
                stock_data = UniverseCRUD.all_stocks[ticker]
                universe_stocks.append({"ticker": stock_data["ticker"], "name": stock_data["name"]})

            universe_create = UniverseCreate(
                name=zone,
                month=month,
                stocks=universe_stocks
            )
            UniverseCRUD.create_universe(db=db, universe=universe_create)

    @staticmethod
    def create_random_universes(db: Session):
        for month in UniverseCRUD.date_range:
            UniverseCRUD.create_random_universe_for_month(db, month)