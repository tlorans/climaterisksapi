from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class StockBase(BaseModel):
    ticker: str
    name: str

class StockCreate(StockBase):
    pass

class Stock(StockBase):
    id: int
    universe_id: int

    class Config:
        orm_mode: True

class UniverseBase(BaseModel):
    name: str
    month: date

class UniverseCreate(UniverseBase):
    stocks: List[StockCreate]

class Universe(UniverseBase):
    id: int
    stocks: List[Stock] = []

    class Config:
        orm_mode: True
