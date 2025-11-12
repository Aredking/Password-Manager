from src.database.dao import UserDAO, AccountDAO
from src.database.entities import Account

user_dao = UserDAO()
acc_dao = AccountDAO()

user, = user_dao.get_all_users()
# acc_dao.add_account(Account("Mail", "email", "pass"), user.id)

accounts = acc_dao.get_all_accounts(user.id)

print(*accounts, sep='\n')