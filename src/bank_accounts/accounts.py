# accounts.py

"""
Реестр банковских счетов
"""
from __future__ import annotations

from pathlib import Path

from rich.table import Table

# Максимальная сумма на счете по умолчанию
DEFAULT_MAX_LIMIT = 1000000.00

# Минимальная сумма на счете по умолчанию
DEFAULT_MIN_LIMIT = -10000.00

# Допустимые типы счетов
ACC_TYPE_SAVING = "S"
ACC_TYPE_CURRENT = "C"


class AccountDict(dict[str, "Account"]):
    """
    Реестр банковских счетов
    """

    def __getitem__(self, key):
        try:
            val = dict.__getitem__(self, key)
            return val
        except Exception:
            raise ValueError(f"Счет с номером #{key} не найден.")

    def append(self, acc: Account) -> None:
        """
        Добавление счета в реестр.
        Ошибка, если номер счета уже есть в реестре.
        """
        if acc.account_number in self.keys():
            raise ValueError(f"Счет с номером {acc.account_number} уже существует.")
        self[acc.account_number] = acc

    def save(self, file_name: Path) -> None:
        """
        Сохранение списка счетов в указанный файл.
        Если файл уже существует, он будет перезаписан.
        """
        with open(file_name, "w", encoding="UTF-8") as f:
            for account in list(self.values()):
                f.write(f"{account.dump()}\n")

    @staticmethod
    def load(file_name: Path) -> AccountDict:
        """
        Загрузка списка счетов из файла.
        Возвращает новый реестр счетов.
        """
        items = AccountDict()
        with open(file_name, "r", encoding="UTF-8") as f:
            acc_lines = f.read().splitlines()
            for acc_line in acc_lines:
                acc = Account.load(acc_line)
                items[acc.account_number] = acc
        return items

    def to_table_view(self) -> Table:
        """
        Список всех счетов в виде таблицы
        """

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("#", style="dim", width=6)
        table.add_column("Тип счета", min_width=15)
        table.add_column("Пользователь", min_width=29, justify="left")
        table.add_column("Баланс", min_width=15, justify="right")
        table.add_column("Мин. лимит", min_width=15, justify="right")
        table.add_column("Макс. лимит", min_width=15, justify="right")

        def get_account_type(account_number: str) -> str:
            if account_number[0] == ACC_TYPE_SAVING:
                return "Сберегательный"
            elif account_number[0] == ACC_TYPE_CURRENT:
                return "Текущий"
            return ""

        accounts = self.values()

        for account in accounts:

            acc_type = get_account_type(account.account_number)
            acc_balance = f"{account.balance:.2f}"

            if account.min_limit != DEFAULT_MIN_LIMIT:
                acc_min_limit = f"{account.min_limit:.2f}"
            else:
                acc_min_limit = ""

            if account.max_limit != DEFAULT_MAX_LIMIT:
                acc_max_limit = f"{account.max_limit:.2f}"
            else:
                acc_max_limit = ""

            table.add_row(
                account.account_number,
                acc_type,
                account.customer_name,
                acc_balance,
                acc_min_limit,
                acc_max_limit)

        return table

    def get_next_free_account_number(self, acc_type: str) -> str:
        max_num = 0
        for acc in self.values():
            if acc.account_number[0] != acc_type:
                continue
            account_no = acc.account_number[1:6]
            num = int(account_no)
            if num > max_num:
                max_num = num
        max_num = max_num + 1

        return f"{acc_type}{str(max_num).zfill(5)}"


class Account:
    """
        Супер-класс для банковского счета
    """

    def __init__(self, account_number: str, customer_name: str, balance: float) -> None:
        self.__max_limit = DEFAULT_MAX_LIMIT
        self.__min_limit = DEFAULT_MIN_LIMIT

        self._validate_account(account_number)
        self._validate_customer_name(customer_name)
        self._validate_balance(balance)

        self.__account_num = account_number
        self.__customer_name = customer_name
        self.__balance = balance
        self.__initial_balance = balance

    @property
    def account_number(self) -> str:
        """
        Номер счета
        """
        return self.__account_num

    @property
    def customer_name(self) -> str:
        """ Имя клиента """
        return self.__customer_name

    @property
    def balance(self) -> float:
        """ Баланс по счету """
        return self.__balance

    @property
    def max_limit(self) -> float:
        """ Максимальный лимит по счету """
        return self.__max_limit

    @property
    def min_limit(self) -> float:
        """ Минимальный лимит по счету """
        return self.__min_limit

    def set_limits(self, min_limit: float = 0, max_limit: float = 0) -> None:
        """ Установить лимиты по счету """
        self.__min_limit = min_limit
        self.__max_limit = max_limit

    def set_balance(self, new_balance: float) -> None:
        """ Установить баланс """
        self._validate_balance(new_balance)
        self.__balance = new_balance

    def deposit(self, amount: float) -> None:
        """ Внести депозит """
        new_balance = self.__balance + amount
        self._validate_balance(new_balance)
        self.__balance = new_balance

    def withdraw(self, amount: float) -> None:
        """ Снять деньги """
        new_balance = self.__balance - amount
        self._validate_balance(new_balance)
        self.__balance = new_balance

    def display(self):
        """ Информация по счету """
        print(f"Номер счета: {self.__account_num}")
        print(f"Клиент: {self.__customer_name}")
        print(f"Баланс: {self.__balance:.2f}")
        if self.__min_limit != DEFAULT_MIN_LIMIT:
            print(f"Минимальный лимит: {self.__min_limit:.2f}")
        if self.__max_limit != DEFAULT_MAX_LIMIT:
            print(f"Максимальный лимит: {self.__max_limit:.2f}")

    def dump(self) -> str:
        """
        Выгрузка счета в формате, пригодном для сохранения в файл
        """
        # TODO: Save and restore limits
        if self.__min_limit == DEFAULT_MIN_LIMIT and self.__max_limit == DEFAULT_MAX_LIMIT:
            return f"{self.__account_num}{self.customer_name:29}{self.__initial_balance:15}"
        return f"{self.__account_num}{self.customer_name:29}{self.__initial_balance:15}{self.__min_limit:15}{self.__max_limit:15}"

    @staticmethod
    def load(line: str) -> Account:
        """
        Загрузка/создание счета из строки, прочитанной из файла
        """
        account_no = line[:6]
        customer_name = line[6:35].strip()
        balance = float(line[35:50])
        account: Account
        if account_no[0] == ACC_TYPE_SAVING:
            # создать сберегательный счет
            account = SavingAccount(account_no, customer_name, balance)
        elif account_no[0] == ACC_TYPE_CURRENT:
            # создать текущий счет
            account = CurrentAccount(account_no, customer_name, balance)
        else:
            raise ValueError(f"Некорректный тип счета в строке: {line}")

        Account._set_limits_from_string(account, line)
        return account

    def _validate_account(self, account: str) -> None:
        if len(account) != 6:
            raise ValueError("Номер счета должен содержать 6 символов.")
        for idx, sym in enumerate(account):
            if idx == 0 and sym != ACC_TYPE_SAVING and sym != ACC_TYPE_CURRENT:
                raise ValueError("Первый символ счета должен содержать буквы S или C")
            if idx > 0 and not sym.isdigit():
                raise ValueError("Номер счета должен содержать только цифры.")

    def _validate_customer_name(self, customer_name: str) -> None:
        if len(customer_name.strip()) == 0:
            raise ValueError("Имя пользователя счета должно быть заполнено.")
        if len(customer_name) > 29:
            raise ValueError("Имя пользователя должно быть не более 29 символов.")

    def _validate_balance(self, balance: float) -> None:
        if balance < self.min_limit:
            raise ValueError(f"Достигнуто ограничение по минимальной сумме на счете {self.min_limit}")
        if balance > self.max_limit:
            raise ValueError(f"Достигнуто ограничение по максимальной сумме на счете {self.max_limit}")

    @staticmethod
    def _set_limits_from_string(account: Account, line: str):

        min_limit_str = line[50:65].strip()
        if len(min_limit_str) > 0:
            min_limit = float(min_limit_str)
        else:
            min_limit = DEFAULT_MIN_LIMIT

        max_limit_str = line[65:80].strip()
        if len(max_limit_str) > 0:
            max_limit = float(max_limit_str)
        else:
            max_limit = DEFAULT_MAX_LIMIT

        account.set_limits(min_limit, max_limit)


class SavingAccount(Account):  # inheritance
    """ Сберегательный счет """

    def __init__(self, account_number: str, customer_name: str, balance: float) -> None:
        super().__init__(account_number, customer_name, balance)
        self.__interest = 0.01 / 12

    def display_monthly_statement(self):
        self.set_balance(self.balance * (1 + self.__interest))
        print("Ежемесячная выписка по сберегательному счету ")
        super().display()

    def _validate_account(self, account: str) -> None:
        super()._validate_account(account)
        if account[0] != ACC_TYPE_SAVING:
            raise ValueError("Первый символ сберегательного счета должен содержать букву S")


class CurrentAccount(Account):
    """ Текущий счет """

    def __init__(self, account_number: str, customer_name: str, balance: float) -> None:
        super().__init__(account_number, customer_name, balance)

    def display_monthly_statement(self):
        print("Ежемесячный отчет по текущему счету ")
        super().display()

    def _validate_account(self, account: str) -> None:
        super()._validate_account(account)
        if account[0] != ACC_TYPE_CURRENT:
            raise ValueError("Первый символ текущего счета должен содержать букву C")
