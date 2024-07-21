import mstarpy
import pandas as pd
from datetime import datetime
from typing import List, Dict

def get_funds(term: str, country: str, page_size: int = 40, currency: str = "USD") -> pd.DataFrame:
    response = mstarpy.search_funds(term=term, field=["Name", "fundShareClassId"], country=country, pageSize=page_size, currency=currency)
    return pd.DataFrame(response)

def get_fund_holdings(fund_share_class_id: str, country: str) -> pd.DataFrame:
    fund = mstarpy.Funds(term=fund_share_class_id, country=country)
    holdings = fund.holdings(holdingType="equity")
    return pd.DataFrame(holdings)

def get_fund_returns(fund_share_class_id: str, country: str, start_date: datetime, end_date: datetime, frequency: str = "daily") -> pd.DataFrame:
    fund = mstarpy.Funds(term=fund_share_class_id, country=country)
    history = fund.nav(start_date=start_date, end_date=end_date, frequency=frequency)
    return pd.DataFrame(history)
