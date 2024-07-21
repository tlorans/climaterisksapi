
from app.crud.funds import FundCRUD
from app.db.session import get_db

test = FundCRUD.get_fund_holdings(next(get_db()), 1)
print(test)