from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class StockReturn(Base):
    __tablename__ = "stock_returns"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    ticker = Column(String, index=True)
    return_value = Column(Float)
    universe_id = Column(Integer, ForeignKey("universes.id"))

    universe = relationship("Universe", back_populates="stock_returns")
