from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.funds import FundCRUD
from app.db.session import get_db
from app.schemas.funds import FundBase, HoldingBase, FundReturn

router = APIRouter()

@router.get("/funds/{fund_name}", response_model=FundBase)
def get_fund_by_name(fund_name: str, db: Session = Depends(get_db)):
    fund = FundCRUD.get_fund_by_name(db, fund_name)
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    return fund

@router.get("/funds/{fund_id}/holdings", response_model=List[HoldingBase])
def get_fund_holdings(fund_id: int, db: Session = Depends(get_db)):
    holdings = FundCRUD.get_fund_holdings(db, fund_id)
    if not holdings:
        raise HTTPException(status_code=404, detail="Holdings not found for this fund")
    return holdings

@router.get("/funds/{fund_id}/true_returns", response_model=List[FundReturn])
def get_fund_true_returns(fund_id: int, db: Session = Depends(get_db)):
    true_returns = FundCRUD.get_fund_true_returns(db, fund_id)
    if not true_returns:
        raise HTTPException(status_code=404, detail="True returns not found for this fund")
    return true_returns

@router.get("/funds/", response_model=List[str])
def get_all_fund_names(db: Session = Depends(get_db)):
    try:
        fund_names = FundCRUD.get_all_fund_names(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return [name for (name,) in fund_names]

