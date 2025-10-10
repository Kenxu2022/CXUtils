from prettytable import PrettyTable
from loguru import logger

from credentials.db import DatabaseManager
from credentials.cookie import initializeCookie, deleteCookie

with DatabaseManager() as dbManager:
    result = dbManager.getUsers()

userTable = PrettyTable()
userTable.field_names = ["序号", "账号"]
seq = 0
for item in result:
    userTable.add_row([seq, item[0]])
    seq = seq + 1
print(userTable)
accountNumber = map(int, input("选择要操作的账号，多个账号请用英文逗号隔开：").split(","))
choice = int(input("1-刷新Cookie 2-删除账号，请选择操作："))

if choice == 1:
    for num in accountNumber:
        username = result[num][0]
        with DatabaseManager() as dbManager:
            encpassword = dbManager.getCookie(username)['encpassword']
        initializeCookie(username, encpassword, True)
elif choice == 2:
    for num in accountNumber:
        username = result[num][0]
        deleteCookie(username)
else:
    logger.error("无效选项")
