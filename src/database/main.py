from account_dao import AccountDAO
from src.database.entity import Account

dao = AccountDAO()
dao.delete_by_id(2)

print(*dao.get_all_accounts())
