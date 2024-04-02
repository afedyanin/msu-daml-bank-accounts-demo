# application.py

"""
Реализация бизнес-сценариев приложения.
"""
from __future__ import annotations

import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table

from accounts import AccountDict, Account, SavingAccount, CurrentAccount, ACC_TYPE_SAVING, ACC_TYPE_CURRENT
from transactions import TransactionList, Transaction, TXN_TYPE_DEPOSIT, TXN_TYPE_WITHDRAW

# Файл для хранения счетов
ACCOUNTS_FILE_NAME = Path("data/ACCOUNTS.DAT")

# Файл для хранения транзакций
TRANSACTIONS_FILE_NAME = Path("data/TRANSACTIONS.DAT")


class Application:
    def __init__(self, accounts_file: Path, transactions_file: Path) -> None:
        self.__accounts = AccountDict.load(accounts_file)
        self.__transactions = TransactionList.load(transactions_file)
        self._init_accounts()

    def add_new_account(self, name: str, account_type: str, balance: float) -> Account:
        """
        Создать новый пользовательский счет
        """
        account_num = self.__accounts.get_next_free_account_number(account_type)
        account: Account

        if account_type == ACC_TYPE_SAVING:
            account = SavingAccount(account_num, name, balance)
        elif account_type == ACC_TYPE_CURRENT:
            account = CurrentAccount(account_num, name, balance)
        else:
            raise ValueError(f"Invalid account type: {account_type}")

        self.__accounts.append(account)
        self.save_accounts()
        return account

    def set_limits(self, account_num: str, min_limit: float, max_limit: float) -> Account:
        """
        Установить лимиты по счету
        """
        found_account = self.__accounts[account_num]
        found_account.set_limits(min_limit, max_limit)
        self.save_accounts()
        return found_account

    def deposit(self, account_num: str, amount: float) -> Transaction:
        """
        Внести сумму на счет.
        """

        # проверим, что счет существует
        _ = self.__accounts[account_num]

        txn = Transaction(datetime.datetime.now(), account_num, TXN_TYPE_DEPOSIT, amount)
        self.__transactions.append(txn)
        self._apply_transaction(txn)
        self.save_transactions()
        return txn

    def withdraw(self, account_num: str, amount: float) -> Transaction:
        """
        Снять сумму со счета.
        """

        # проверим, что счет существует
        _ = self.__accounts[account_num]

        txn = Transaction(datetime.datetime.now(), account_num, TXN_TYPE_WITHDRAW, amount)
        self.__transactions.append(txn)
        self._apply_transaction(txn)
        self.save_transactions()
        return txn

    def get_account(self, account_num: str) -> Account:
        """
        Получить информацию по счету.
        """
        return self.__accounts[account_num]

    def get_all_accounts(self) -> Table:
        """
        Получить список всех счетов в виде таблицы.
        """

        return self.__accounts.to_table_view()

    def get_all_transactions(self, account_num: str) -> Table:
        """
        История транзакций по счету.
        """
        return self.__transactions.to_table_view(account_num)

    def save_transactions(self, file_name: Path = TRANSACTIONS_FILE_NAME) -> None:
        """
        Выгрузить историю транзакций в файл.
        """
        self.__transactions.save(file_name)

    def save_accounts(self, file_name: Path = ACCOUNTS_FILE_NAME) -> None:
        """
        Выгрузить счета в файл
        """
        self.__accounts.save(file_name)

    def import_data(self, accounts_file: Path, transactions_file: Path) -> None:
        """
        Импортировать данные из файлов и проинициализировать систему
        """
        self.__transactions.load(transactions_file)
        self.__accounts.load(accounts_file)
        self._init_accounts()

    def _init_accounts(self) -> None:
        for txn in self.__transactions:
            self._apply_transaction(txn)

    def _apply_transaction(self, txn: Transaction) -> None:
        found_account = self.__accounts[txn.account]
        if txn.txn_type == TXN_TYPE_DEPOSIT:
            found_account.deposit(txn.amount)
        if txn.txn_type == TXN_TYPE_WITHDRAW:
            found_account.withdraw(txn.amount)


# start application and load data
bank_app = Application(ACCOUNTS_FILE_NAME, TRANSACTIONS_FILE_NAME)

if __name__ == "__main__":
    console = Console()
    accounts = bank_app.get_all_accounts()
    console.print(accounts)


