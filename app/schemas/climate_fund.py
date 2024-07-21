from pydantic import BaseModel
from datetime import date
from typing import List

class ClimateHoldingBase(BaseModel):
    security_name: str
    weighting: float
    sus_esg_risk_score: float

class ClimateHoldingCreate(ClimateHoldingBase):
    fund_id: int

class ClimateHolding(ClimateHoldingBase):
    id: int
    fund_id: int

    class Config:
        orm_mode: True

class ClimateFundReturnBase(BaseModel):
    date: date
    total_return: float

class ClimateFundReturnCreate(ClimateFundReturnBase):
    fund_id: int

class ClimateFundReturn(ClimateFundReturnBase):
    id: int
    fund_id: int

    class Config:
        orm_mode: True

class ClimateFundBase(BaseModel):
    name: str
    fund_share_class_id: str

class ClimateFundCreate(ClimateFundBase):
    holdings: List[ClimateHoldingCreate] = []
    returns: List[ClimateFundReturnCreate] = []

class ClimateFund(ClimateFundBase):
    id: int
    holdings: List[ClimateHolding] = []
    returns: List[ClimateFundReturn] = []

    class Config:
        orm_mode: True
