from pydantic import BaseModel
from datetime import date
from typing import List

class HoldingBase(BaseModel):
    security_name: str
    weighting: float
    sus_esg_risk_score: float

class HoldingCreate(HoldingBase):
    fund_id: int

class Holding(HoldingBase):
    id: int
    fund_id: int

    class Config:
        orm_mode: True

class FundReturnBase(BaseModel):
    date: date
    total_return: float

class FundReturnCreate(FundReturnBase):
    fund_id: int

class FundReturn(FundReturnBase):
    id: int
    fund_id: int

    class Config:
        orm_mode: True

class FundBase(BaseModel):
    name: str
    fund_share_class_id: str

class FundCreate(FundBase):
    holdings: List[HoldingCreate] = []
    returns: List[FundReturnCreate] = []

class Fund(FundBase):
    id: int
    holdings: List[Holding] = []
    returns: List[FundReturn] = []

    class Config:
        orm_mode: True
