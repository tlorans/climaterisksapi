from pydantic import BaseModel
from datetime import date

class ClimateNewsBase(BaseModel):
    date: date
    name: str
    value: float

class ClimateNewsCreate(ClimateNewsBase):
    pass

class ClimateNews(ClimateNewsBase):
    id: int

    class Config:
        orm_mode: True
