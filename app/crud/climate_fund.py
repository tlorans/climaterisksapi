from sqlalchemy.orm import Session
from app.models.climate_fund import ClimateFund, ClimateHolding, ClimateFundReturn
from app.schemas.climate_fund import ClimateFundCreate, ClimateHoldingCreate, ClimateFundReturnCreate
from app.scraper.scraper import get_funds, get_fund_holdings, get_fund_returns
from datetime import datetime
from tqdm import tqdm

class ClimateFundCRUD:
    @staticmethod
    def create_climate_fund(db: Session, fund: ClimateFundCreate):
        db_fund = ClimateFund(name=fund.name, fund_share_class_id=fund.fund_share_class_id)
        db.add(db_fund)
        db.commit()
        db.refresh(db_fund)
        return db_fund

    @staticmethod
    def create_climate_holdings_bulk(db: Session, holdings: list):
        db.bulk_save_objects(holdings)
        db.commit()

    @staticmethod
    def create_climate_fund_returns_bulk(db: Session, fund_returns: list):
        db.bulk_save_objects(fund_returns)
        db.commit()

    @staticmethod
    def get_climate_fund(db: Session, fund_share_class_id: str):
        return db.query(ClimateFund).filter(ClimateFund.fund_share_class_id == fund_share_class_id).first()

    @staticmethod
    def get_climate_funds(db: Session, skip: int = 0, limit: int = 100):
        return db.query(ClimateFund).offset(skip).limit(limit).all()

    @staticmethod
    def populate_climate_funds(db: Session, fund_share_class_ids: list, start_date: datetime, end_date: datetime):
        for fund_share_class_id in tqdm(fund_share_class_ids, desc="Populating climate funds"):
            fund_info = get_funds(term=fund_share_class_id, country="us", page_size=1, currency="usd")
            if fund_info.empty:
                continue
            row = fund_info.iloc[0]
            fund = ClimateFundCreate(name=row["Name"], fund_share_class_id=row["fundShareClassId"])
            db_fund = ClimateFundCRUD.create_climate_fund(db, fund)

            holdings_df = get_fund_holdings(row["fundShareClassId"], "us")
            holdings = []
            for _, holding_row in holdings_df.iterrows():
                holding = ClimateHolding(
                    fund_id=db_fund.id,
                    security_name=holding_row["securityName"],
                    weighting=holding_row["weighting"],
                    sus_esg_risk_score=holding_row["susEsgRiskScore"]
                )
                holdings.append(holding)
            ClimateFundCRUD.create_climate_holdings_bulk(db, holdings)

            returns_df = get_fund_returns(row["fundShareClassId"], "us", start_date, end_date)
            fund_returns = []
            for _, return_row in returns_df.iterrows():
                fund_return = ClimateFundReturn(
                    fund_id=db_fund.id,
                    date=datetime.strptime(return_row["date"], '%Y-%m-%d').date(),  # Convert to datetime.date
                    total_return=return_row["totalReturn"]
                )
                fund_returns.append(fund_return)
            ClimateFundCRUD.create_climate_fund_returns_bulk(db, fund_returns)
