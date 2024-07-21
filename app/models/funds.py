from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Fund(Base):
    __tablename__ = "funds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    fund_share_class_id = Column(String, unique=True, index=True)

    holdings = relationship("Holding", back_populates="fund")
    returns = relationship("FundReturn", back_populates="fund")

class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("funds.id"))
    security_name = Column(String)
    weighting = Column(Float)
    sus_esg_risk_score = Column(Float)

    fund = relationship("Fund", back_populates="holdings")

class FundReturn(Base):
    __tablename__ = "fund_returns"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("funds.id"))
    date = Column(Date, index=True)
    total_return = Column(Float)

    fund = relationship("Fund", back_populates="returns")
