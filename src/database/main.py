from account_dao import AccountDAO
from src.database.entity import Account

dao = AccountDAO()
# Поддерживаются следующие операции:
# Получения всех записей из БД
# Добавление записи
# Удаление по id

print(*dao.get_all_accounts())
