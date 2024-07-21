from pydantic import BaseModel
from datetime import date
from typing import List

class StockReturnBase(BaseModel):
    date: date
    ticker: str
    return_value: float

class StockReturnCreate(StockReturnBase):
    universe_id: int

class StockReturn(StockReturnBase):
    id: int
    universe_id: int

    class Config:
        orm_mode: True
