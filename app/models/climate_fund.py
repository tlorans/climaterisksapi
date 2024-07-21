from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class ClimateFund(Base):
    __tablename__ = "climate_funds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    fund_share_class_id = Column(String, unique=True, index=True)

    holdings = relationship("ClimateHolding", back_populates="fund")
    returns = relationship("ClimateFundReturn", back_populates="fund")
    climate_signals = relationship("ClimateSignal", back_populates="fund")

class ClimateHolding(Base):
    __tablename__ = "climate_holdings"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("climate_funds.id"))
    security_name = Column(String)
    weighting = Column(Float)
    sus_esg_risk_score = Column(Float)

    fund = relationship("ClimateFund", back_populates="holdings")

class ClimateFundReturn(Base):
    __tablename__ = "climate_fund_returns"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("climate_funds.id"))
    date = Column(Date, index=True)
    total_return = Column(Float)

    fund = relationship("ClimateFund", back_populates="returns")
