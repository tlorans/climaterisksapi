from sqlalchemy.orm import Session
from app.models.funds import Fund, Holding, FundReturn
from app.schemas.funds import FundCreate, HoldingCreate, FundReturnCreate
from app.scraper.scraper import get_funds, get_fund_holdings, get_fund_returns
from datetime import datetime
from tqdm import tqdm

class FundCRUD:
    @staticmethod
    def create_fund(db: Session, fund: FundCreate):
        db_fund = Fund(name=fund.name, fund_share_class_id=fund.fund_share_class_id)
        db.add(db_fund)
        db.commit()
        db.refresh(db_fund)
        return db_fund

    @staticmethod
    def create_holdings_bulk(db: Session, holdings: list):
        db.bulk_save_objects(holdings)
        db.commit()

    @staticmethod
    def create_fund_returns_bulk(db: Session, fund_returns: list):
        db.bulk_save_objects(fund_returns)
        db.commit()

    @staticmethod
    def get_fund(db: Session, fund_share_class_id: str):
        return db.query(Fund).filter(Fund.fund_share_class_id == fund_share_class_id).first()

    @staticmethod
    def get_funds(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Fund).offset(skip).limit(limit).all()

    @staticmethod
    def populate_funds(db: Session, term: str, country: str, page_size: int, currency: str, start_date: datetime, end_date: datetime):
        funds_df = get_funds(term, country, page_size, currency)
        print(f"Columns in funds_df: {funds_df.columns}")  # Add this line to verify column names

        for _, row in tqdm(funds_df.iterrows(), total=funds_df.shape[0], desc="Populating funds"):
            fund = FundCreate(name=row["Name"], fund_share_class_id=row["fundShareClassId"])
            db_fund = FundCRUD.create_fund(db, fund)
            
            holdings_df = get_fund_holdings(row["fundShareClassId"], country)
            holdings = []
            for _, holding_row in holdings_df.iterrows():
                holding = Holding(
                    fund_id=db_fund.id,
                    security_name=holding_row["securityName"],
                    weighting=holding_row["weighting"],
                    sus_esg_risk_score=holding_row["susEsgRiskScore"]
                )
                holdings.append(holding)
            FundCRUD.create_holdings_bulk(db, holdings)
            
            returns_df = get_fund_returns(row["fundShareClassId"], country, start_date, end_date)
            fund_returns = []
            for _, return_row in returns_df.iterrows():
                fund_return = FundReturn(
                    fund_id=db_fund.id,
                    date=datetime.strptime(return_row["date"], '%Y-%m-%d').date(),  # Convert to datetime.date
                    total_return=return_row["totalReturn"]
                )
                fund_returns.append(fund_return)
            FundCRUD.create_fund_returns_bulk(db, fund_returns)
