import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.models.climate_fund import ClimateFundReturn
from app.models.climate_news import ClimateNews
from statsmodels.regression.rolling import RollingOLS
import statsmodels.api as sm
from app.models.climate_signal import ClimateSignal
from app.schemas.climate_signal import ClimateSignalCreate

class ClimateSignalCRUD:
    @staticmethod
    def get_climate_fund_returns(db: Session):
        query = db.query(ClimateFundReturn.fund_id, ClimateFundReturn.date, ClimateFundReturn.total_return).all()
        df = pd.DataFrame(query, columns=['fund_id', 'date', 'total_return'])
        df['date'] = pd.to_datetime(df['date'])
        # Compute the first differences (returns) for each fund
        df.sort_values(by=['fund_id', 'date'], inplace=True)
        df['total_return'] = df['total_return'] / 100
        df['total_return'] = df.groupby('fund_id')['total_return'].diff()
        df.dropna(inplace=True)
        return df

    @staticmethod
    def get_climate_news_series_by_name(db: Session, name: str):
        query = db.query(ClimateNews.date, ClimateNews.value).filter(ClimateNews.name == name).all()
        df = pd.DataFrame(query, columns=['date', 'value'])
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        # Compute the first differences (returns) for the climate news series
        df['value'] = df['value'].diff()
        df.dropna(inplace=True)

        return df

    @staticmethod
    def get_market_factors(file_path: str):
        df = pd.read_csv(file_path, parse_dates=['date'])
        df.set_index('date', inplace=True)
        return df

    @staticmethod
    def calculate_rolling_beta(df, y_col, x_col, window=252):
        model = RollingOLS(df[y_col], df[x_col], window=window)
        rres = model.fit()
        return rres.params

    @staticmethod
    def create_climate_signal(db: Session, climate_signal: ClimateSignalCreate):
        db_climate_signal = ClimateSignal(**climate_signal.dict())
        db.add(db_climate_signal)
        db.commit()
        db.refresh(db_climate_signal)
        return db_climate_signal

    @staticmethod
    def create_climate_signals_bulk(db: Session, climate_signals: list):
        db.bulk_save_objects(climate_signals)
        db.commit()


    @staticmethod
    def generate_climate_factor_signal(db: Session, climate_news_name: str):
        fund_returns = ClimateSignalCRUD.get_climate_fund_returns(db)
        climate_news = ClimateSignalCRUD.get_climate_news_series_by_name(db, climate_news_name)

        # Find the common dates across all dataframes
        common_dates = fund_returns['date'].unique()
        common_dates = pd.to_datetime(common_dates)
        climate_news = climate_news[climate_news.index.isin(common_dates)]
        fund_returns = fund_returns[fund_returns['date'].isin(common_dates)]

        all_signals = []
        df_results = pd.DataFrame()
        for fund_id in fund_returns['fund_id'].unique():
            fund_data = fund_returns[fund_returns['fund_id'] == fund_id].set_index('date')
            combined_data = fund_data.join(climate_news, how='inner').dropna()

            print(f"Processing fund_id: {fund_id}")

            if combined_data.shape[0] < 252:
                print(f"Not enough data for fund_id {fund_id}")
                continue

            # Check for NaNs in combined_data
            if combined_data.isnull().values.any():
                print(f"NaNs found in combined_data for fund_id {fund_id}")
                print(combined_data.isnull().sum())
                continue

            betas = ClimateSignalCRUD.calculate_rolling_beta(
                combined_data, 
                y_col='total_return', 
                x_col='value'
            )

            betas = betas.dropna()

            print(f"Betas for fund_id {fund_id}:\n{betas.head()}")
            # Apply the rescaling to get the signal
            betas['positive_beta'] = betas['value'].apply(lambda x: max(x, 0))
            betas['fund_id'] = fund_id
            df_results = pd.concat([df_results, betas])
        
        df_results['weight'] = df_results.groupby('date')['positive_beta'].transform(lambda x: x / x.sum())

        for date, row in df_results.iterrows():
            signal = ClimateSignalCreate(
                fund_id=row['fund_id'],
                date=date,
                beta=row['weight']
            )
            all_signals.append(ClimateSignal(**signal.dict()))

        ClimateSignalCRUD.create_climate_signals_bulk(db, all_signals)

        print("Climate signals have been saved to the database.")