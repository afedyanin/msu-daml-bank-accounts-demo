# transactions.py

"""
Реестр транзакций по банковским счетам
"""

from __future__ import annotations
import datetime

from rich.table import Table
from accounts import ACC_TYPE_SAVING, ACC_TYPE_CURRENT

# Формат даты, используемый для сохранения и загрузки транзакций
# Пример 20120713
DATE_FORMAT = "%Y%m%d"

# Допустимые типы транзакций
TXN_TYPE_DEPOSIT = "D"
TXN_TYPE_WITHDRAW = "W"


class TransactionList(list["Transaction"]):
    """
    Реестр транзакций в виде списка
    """

    def search(self, account_num: str) -> list["Transaction"]:
        """
        Поиск транзакций по номеру счета
        """
        matching_items: list["Transaction"] = []
        for txn in self:
            if account_num == txn.account:
                matching_items.append(txn)
        return matching_items

    def save(self, file_name: str) -> None:
        """
        Сохранение списка транзакций в указанный файл.
        Если файл уже существует, он будет перезаписан.
        """
        with open(file_name, "w", encoding="UTF-8") as f:
            for txn in self:
                f.write(f"{txn.dump()}\n")

    @staticmethod
    def load(file_name: str) -> TransactionList:
        """
        Загрузка списка транзакций из файла.
        Возвращает новый реестр транзакций.
        """
        items = TransactionList()
        with open(file_name, "r", encoding="UTF-8") as f:
            txn_lines = f.read().splitlines()
            for txn_line in txn_lines:
                txn = Transaction.load(txn_line)
                items.append(txn)
        return items

    def to_table_view(self, account_num: str) -> Table:
        """
        Список всех транзакций в виде таблицы
        """

        table = Table(show_header=True, header_style="bold green")
        table.add_column("Дата", style="dim", width=10)
        table.add_column("Счет #", style="dim", width=6)
        table.add_column("Депозит", min_width=15, justify="right")
        table.add_column("Списание", min_width=15, justify="right")

        if account_num is None:
            transactions = self
        else:
            transactions = self.search(account_num)

        for txn in transactions:

            date = txn.date.strftime("%Y-%m-%d")
            acc_num = txn.account

            if txn.txn_type == TXN_TYPE_DEPOSIT:
                depo = f"{txn.amount:.2f}"
            else:
                depo = ""

            if txn.txn_type == TXN_TYPE_WITHDRAW:
                withdraw = f"{txn.amount:.2f}"
            else:
                withdraw = ""

            table.add_row(date, acc_num, depo, withdraw)

        return table


class Transaction:
    """
    Транзакция по счету
    """

    def __init__(self, date: datetime.datetime, account: str, txn_type: str, amount: float) -> None:

        self._validate_account(account)
        self._validate_txn_type(txn_type)
        self._validate_amount(amount)

        self.__date = date.date()
        self.__account = account
        self.__txn_type = txn_type
        self.__amount = amount

    @property
    def date(self) -> datetime.date:
        """
        Дата транзакции.
        """
        return self.__date

    @property
    def account(self) -> str:
        """
        Номер счета. 6 символов.
        Первый символ - тип счета:
            S - Savings - сберегательный счет
            C - Current - текущий счет
        Остальные пять символов - цифры
        """
        return self.__account

    @property
    def txn_type(self) -> str:
        """
        Тип транзакции. Допустимые значения:
            D - Deposit - внесение суммы
            W - Withdrawal - снятие суммы
        """
        return self.__txn_type

    @property
    def amount(self) -> float:
        """
        Сумма транзакции
        """
        return self.__amount

    def dump(self) -> str:
        """
        Выгрузка транзакции в формате, пригодном для сохранения в файл
        """
        return f"{self.__date.strftime(DATE_FORMAT)}{self.__account}{self.__txn_type}{self.__amount:15}"

    @staticmethod
    def load(line: str) -> Transaction:
        """
        Загрузка/создание транзакции из строки, прочитанной из файла
        """
        date = datetime.datetime.strptime(line[:8], DATE_FORMAT)
        account = line[8:14]
        txn_type = line[14:15]
        amount = float(line[15:])
        return Transaction(date, account, txn_type, amount)

    # Валидация бизнес-правил и инварианты

    @staticmethod
    def _validate_txn_type(txn_type: str) -> None:
        if txn_type == TXN_TYPE_DEPOSIT or txn_type == TXN_TYPE_WITHDRAW:
            return
        raise ValueError(f"Неизвестный тип транзакции: {txn_type}")

    @staticmethod
    def _validate_account(account: str) -> None:
        # TODO: Move it to account class ?
        if len(account) != 6:
            raise ValueError("Номер счета должен содержать 6 символов.")
        for idx, sym in enumerate(account):
            if idx == 0 and sym != ACC_TYPE_SAVING and sym != ACC_TYPE_CURRENT:
                raise ValueError("Первый символ счета должен содержать буквы S или C")
            if idx > 0 and not sym.isdigit():
                raise ValueError("Номер счета должен содержать только цифры.")

    @staticmethod
    def _validate_amount(amount: float):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной.")
