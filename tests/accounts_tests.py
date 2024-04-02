# accounts_tests.py

"""
Тест кейсы для объектов банковских счетов и реестра счетов
"""

import unittest
import os
from pathlib import Path
from unittest import expectedFailure, TestCase

from bank_accounts.accounts import CurrentAccount, SavingAccount, AccountDict, DEFAULT_MIN_LIMIT, DEFAULT_MAX_LIMIT


class TestAccount(TestCase):

    def test_create_saving_account(self):
        """
        Создание нового сберегательного счета
        """
        account = "S12345"
        customer_name = "Владимир Петров"
        balance = 213.98

        acc = SavingAccount(account, customer_name, balance)

        self.assertEqual(acc.account_number, account)
        self.assertEqual(acc.customer_name, customer_name)
        self.assertEqual(acc.balance, balance)

    def test_invalid_saving_account_type(self):
        """
        Некорректный тип счета
        """
        self.assertRaises(ValueError, SavingAccount, "С12345", "Владимир Петров", 213.98)

    def test_invalid_saving_account_number(self):
        """
        Некорректный номер счета
        """
        self.assertRaises(ValueError, SavingAccount, "S045AA", "Владимир Петров", 213.98)

    def test_create_current_account(self):
        """
        Создание нового текущего счета
        """
        account = "C12345"
        customer_name = "Иван Стулов"
        balance = 987.36

        acc = CurrentAccount(account, customer_name, balance)

        self.assertEqual(acc.account_number, account)
        self.assertEqual(acc.customer_name, customer_name)
        self.assertEqual(acc.balance, balance)

    def test_invalid_current_account_type(self):
        """
        Некорректный тип счета
        """
        self.assertRaises(ValueError, CurrentAccount, "W12345", "Владимир Петров", 213.98)

    def test_invalid_current_account_number(self):
        """
        Некорректный номер счета
        """
        self.assertRaises(ValueError, CurrentAccount, "C0045", "Владимир Петров", 213.98)

    def test_invalid_customer_name(self):
        """
        Некорректное имя клиента
        """
        self.assertRaises(ValueError, CurrentAccount, "С12345", "    ", 213.98)

    def test_set_balance(self):
        """
        Корректировка баланса
        """
        acc = CurrentAccount("C12345", "Иван Стулов", 987.36)
        new_balance = 3456.18
        acc.set_balance(new_balance)

        self.assertEqual(acc.balance, new_balance)

    def test_set_invalid_balance(self):
        """
        Отрицательная сумма баланса
        """
        acc = CurrentAccount("C12345", "Иван Стулов", 987.36)
        new_balance = -3456.18
        acc.set_balance(new_balance)

        self.assertEqual(acc.balance, new_balance)

    def test_deposit_withdraw(self):
        """
        Внесение депозита на счет и снятие денег
        """
        acc = CurrentAccount("C12345", "Иван Стулов", 100.00)
        acc.deposit(30)
        self.assertEqual(acc.balance, 100 + 30)

        acc.withdraw(50)
        self.assertEqual(acc.balance, 130 - 50)

    def test_invalid_withdraw(self):
        """
        Превышение суммы снятия
        """
        acc = CurrentAccount("C12345", "Иван Стулов", 100.00)
        acc.deposit(30)
        acc.withdraw(150)
        self.assertEqual(acc.balance, 100+30-150)

    def test_set_limits_max(self):
        """
        Превышение лимита по максимальной сумме
        """
        acc = CurrentAccount("C12345", "Иван Стулов", 100.00)
        acc.set_limits(20, 120)

        self.assertRaises(ValueError, acc.deposit, 200)

    def test_set_limits_min(self):
        """
        Превышение лимита по минимальной сумме
        """
        acc = CurrentAccount("C12345", "Иван Стулов", 100.00)
        acc.set_limits(20, 120)

        self.assertRaises(ValueError, acc.withdraw, 95)


class TestAccountList(TestCase):
    def setUp(self):
        self.accounts = AccountDict()

    def test_add_account(self):
        """
        Добавить новый счет в реестр
        """
        account = "S12345"
        customer_name = "Галина Табуреткина"
        balance = 123.56

        acc = SavingAccount(account, customer_name, balance)
        self.accounts.append(acc)
        self.assertEqual(len(self.accounts), 1)

    def test_add_account_twice(self):
        """
        Добавить повторно счет с уже существующим номером
        """
        account = "S12345"
        customer_name = "Галина Табуреткина"
        balance = 123.56

        acc = SavingAccount(account, customer_name, balance)
        self.accounts.append(acc)

        self.assertRaises(ValueError, self.accounts.append, acc)

    def test_search_account(self):
        """
        Найти счет по номеру
        """
        account = "C12345"
        customer_name = "Галина Табуреткина"
        balance = 123.56
        self.accounts.append(CurrentAccount("C54312", customer_name, 123.45))
        self.accounts.append(CurrentAccount(account, customer_name, balance))
        self.accounts.append(SavingAccount("S06789", customer_name, 3))

        found = self.accounts.get(account)
        self.assertEqual(found.account_number, account)

    def test_save_accounts(self):
        """
        Сохранить реестр счетов в файл
        """
        self.accounts.append(SavingAccount("S12345", "Иван Петров", 123.45))
        self.accounts.append(CurrentAccount("C00001", "Петр Иванов", 1320.56))
        self.accounts.append(SavingAccount("S00001", "Иван Сидоров", 1320.56))

        filename = Path("accounts_tst.dat")
        self.accounts.save(filename)

        self.assertTrue(os.path.isfile(filename))

    def test_load_accounts(self):
        """
        Загрузить реестр счетов из файла и сравнить с первоначальным списком
        """
        self.accounts.append(SavingAccount("S12345", "Иван Петров", 123.45))
        self.accounts.append(CurrentAccount("C00001", "Петр Иванов", 1320.56))
        self.accounts.append(SavingAccount("S00001", "Иван Сидоров", 1320.56))

        filename = Path("accounts_tst.dat")
        self.accounts.save(filename)

        loaded = AccountDict.load(filename)
        self.assertEqual(len(loaded), len(self.accounts))

        for acc in self.accounts.values():
            found = loaded.get(acc.account_number)
            self.assertIsNotNone(found)
            self.assertEqual(acc.customer_name, found.customer_name)
            self.assertEqual(acc.balance, found.balance)

    def test_get_next_account_number(self):
        s_num = self.accounts.get_next_free_account_number("S")
        self.assertEqual(s_num, "S00001")

        c_num = self.accounts.get_next_free_account_number("C")
        self.assertEqual(c_num, "C00001")

        self.accounts.append(SavingAccount("S12345", "Иван Петров", 123.45))
        self.accounts.append(CurrentAccount("C00341", "Петр Иванов", 1320.56))
        self.accounts.append(SavingAccount("S00001", "Иван Сидоров", 1320.56))

        s_num = self.accounts.get_next_free_account_number("S")
        self.assertEqual(s_num, "S12346")

        c_num = self.accounts.get_next_free_account_number("C")
        self.assertEqual(c_num, "C00342")

    def test_save_account_with_limits(self):
        """
        Сохранить и загрузить счета с установленными лимитами
        """

        acc = SavingAccount("S12345", "Галина Табуреткина", 123.56)
        acc.set_limits(20.45, 2000.17)
        self.accounts.append(acc)

        acc2 = CurrentAccount("C12345", "Андрей Первый", 1230)
        self.accounts.append(acc2)

        filename = Path("accounts_tst.dat")
        self.accounts.save(filename)

        new_dict = self.accounts.load(filename)

        acc_loaded = new_dict.get("S12345")
        acc2_loaded = new_dict.get("C12345")

        self.assertEqual(acc_loaded.min_limit, 20.45)
        self.assertEqual(acc_loaded.max_limit, 2000.17)

        self.assertEqual(acc2_loaded.min_limit, DEFAULT_MIN_LIMIT)
        self.assertEqual(acc2_loaded.max_limit, DEFAULT_MAX_LIMIT)


# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
