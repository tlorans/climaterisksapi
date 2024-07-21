from sqlalchemy.orm import Session
from app.models.climate_news import ClimateNews
from app.schemas.climate_news import ClimateNewsCreate
import pandas as pd

class ClimateNewsCRUD:
    @staticmethod
    def create_climate_news(db: Session, climate_news: ClimateNewsCreate):
        db_climate_news = ClimateNews(**climate_news.dict())
        db.add(db_climate_news)
        db.commit()
        db.refresh(db_climate_news)
        return db_climate_news

    @staticmethod
    def create_climate_news_bulk(db: Session, climate_news_list: list):
        db.bulk_save_objects(climate_news_list)
        db.commit()

    @staticmethod
    def populate_climate_news(db: Session, file_path: str):
        df = pd.read_excel(file_path, sheet_name='2023 update daily', skiprows=6)  # Skip the first 6 rows

        # Convert column names to lowercase and replace spaces with underscores
        df.columns = df.columns.str.lower().str.replace(' ', '_')

        all_news = []

        for _, row in df.iterrows():
            date = pd.to_datetime(row['date'], dayfirst=True).date()
            for column in df.columns[1:]:
                climate_news = ClimateNews(
                    date=date,
                    name=column,
                    value=row[column]
                )
                all_news.append(climate_news)

        # Bulk insert all climate news
        ClimateNewsCRUD.create_climate_news_bulk(db, all_news)
