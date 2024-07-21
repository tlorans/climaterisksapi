from pydantic import BaseModel
from datetime import date

class ClimateSignalCreate(BaseModel):
    fund_id: int
    date: date
    beta: float
