from sqlalchemy import Column, Integer, String, Date, Float
from app.db.base import Base

class ClimateNews(Base):
    __tablename__ = "climate_news"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    name = Column(String, index=True)
    value = Column(Float)
