
from app.crud.funds import FundCRUD
from app.db.session import get_db

test = FundCRUD.get_all_fund_names(next(get_db()))
print([name for (name,) in test])   