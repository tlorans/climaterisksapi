from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class ClimateSignal(Base):
    __tablename__ = "climate_signals"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("climate_funds.id"), index=True)
    date = Column(Date, index=True)
    beta = Column(Float)

    fund = relationship("ClimateFund", back_populates="climate_signals")
