from sqlalchemy.orm import Session
from app.models.returns import StockReturn
from app.schemas.returns import StockReturnCreate
from app.models.universe import Universe
from datetime import date
import random
from tqdm import tqdm

class StockReturnCRUD:
    @staticmethod
    def create_stock_return(db: Session, stock_return: StockReturnCreate):
        db_stock_return = StockReturn(**stock_return.dict())
        db.add(db_stock_return)
        db.commit()
        db.refresh(db_stock_return)
        return db_stock_return

    @staticmethod
    def get_stock_returns(db: Session, date: date, universe_id: int):
        return db.query(StockReturn).filter(StockReturn.date == date, StockReturn.universe_id == universe_id).all()

    @staticmethod
    def get_all_stock_returns(db: Session, skip: int = 0, limit: int = 100):
        return db.query(StockReturn).offset(skip).limit(limit).all()

    @staticmethod
    def populate_stock_returns(db: Session):
        # Get distinct dates from the Universe table
        dates = db.query(Universe.month).distinct().all()
        dates = [record[0] for record in dates]

        # Simulate monthly returns for each date
        for date in tqdm(dates, desc="Populating stock returns"):
            # Get all stocks for the given date
            universes = db.query(Universe).filter(Universe.month == date).all()
            for universe in universes:
                stock_list = [stock.ticker for stock in universe.stocks]
                for stock in stock_list:
                    monthly_return = round(random.uniform(-0.2, 0.2), 4)
                    stock_return_create = StockReturnCreate(
                        date=date,
                        ticker=stock,
                        return_value=monthly_return,
                        universe_id=universe.id
                    )
                    StockReturnCRUD.create_stock_return(db=db, stock_return=stock_return_create)