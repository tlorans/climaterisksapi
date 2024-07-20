from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.base import Base

class Universe(Base):
    __tablename__ = "universes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    month = Column(Date, index=True)
    stocks = relationship("Stock", back_populates="universe")

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    name = Column(String, index=True)
    universe_id = Column(Integer, ForeignKey("universes.id"))
    universe = relationship("Universe", back_populates="stocks")
