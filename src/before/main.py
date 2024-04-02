from classes import *

# открыть файлы для ввода
account_file = open("data/ACCOUNTS.DAT", 'r')
transaction_file = open("data/TRANSACTIONS.DAT", 'r')

# прочитать все строки из файла аккаунта
account_lines = account_file.readlines()

# прочитать все строки из файла транзакции
transaction_lines = transaction_file.readlines()

# просмотреть все учетные записи
for account_line in account_lines:
    # получить данные аккаунта
    account_no = account_line[:6]
    customer_name = account_line[6:35]
    balance = float(account_line[35:])
    if account_no[0] == 'S':
        # создать объект сохранения аккаунта
        account = SavingAccount(account_no, customer_name, balance)
    else:
        # создать объект текущего счета
        account = CurrentAccount(account_no, customer_name, balance)
    # account.display()

    # пройти через все транзакции
    for transaction_line in transaction_lines:
        # получить детали транзакции
        transaction_date = transaction_line[:8]
        transaction_account = transaction_line[8:14]
        transaction_type = transaction_line[14:15]
        transaction_amount = float(transaction_line[15:])
        # если соответствующий аккаунт
        if transaction_account == account_no:
            if transaction_type == 'D':  # депозит
                account.deposit(transaction_amount)
            else:  # списание
                account.withdraw(transaction_amount)

    # вывод ежемесячного отчета
    account.display_monthly_statement()
    print()

# close files
account_file.close()
transaction_file.close()
