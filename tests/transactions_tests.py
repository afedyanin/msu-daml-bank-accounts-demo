# transactions_tests.py

"""
Тест кейсы для объектов транзакций и реестра транзакций
"""

import datetime
import unittest
import os
from unittest import expectedFailure, TestCase

from bank_accounts.src.bank_accounts.transactions import Transaction, TransactionList


class TestTransaction(TestCase):

    def test_create_transaction(self):
        """
        Создание новой транзакции
        """
        account = "S12345"
        txn_type = "D"
        amount = 123.56
        date = datetime.datetime.now()

        txn = Transaction(date, account, txn_type, amount)

        self.assertEqual(txn.date, date.date())
        self.assertEqual(txn.account, account)
        self.assertEqual(txn.txn_type, txn_type)
        self.assertEqual(txn.amount, amount)

    @expectedFailure
    def test_invalid_txn_type(self):
        """ Неправильный тип транзакции """
        account = "S12345"
        txn_type = "X"
        amount = 123.56
        date = datetime.datetime.now()

        txn = Transaction(date, account, txn_type, amount)
        self.assertEqual(txn.txn_type, txn_type)

    @expectedFailure
    def test_invalid_amount(self):
        """ Некорректная сумма """
        account = "S12345"
        txn_type = "D"
        amount = -123.56
        date = datetime.datetime.now()

        txn = Transaction(date, account, txn_type, amount)
        self.assertEqual(txn.txn_type, txn_type)

    @expectedFailure
    def test_invalid_account(self):
        """ Некорректный номер счета """
        account = "12ABC5E"
        txn_type = "D"
        amount = 123.56
        date = datetime.datetime.now()

        txn = Transaction(date, account, txn_type, amount)
        self.assertEqual(txn.txn_type, txn_type)


class TestTransactionList(TestCase):
    def setUp(self):
        self.transactions = TransactionList()

    def test_add_transaction(self):
        """
        Добавить новую транзакцию в список
        """
        account = "S12345"
        txn_type = "D"
        amount = 123.56
        date = datetime.datetime.now()
        txn = Transaction(date, account, txn_type, amount)

        self.transactions.append(txn)
        self.assertEqual(len(self.transactions), 1)

    def test_search_transactions(self):
        """
        Найти все транзакции по указанному номеру счета
        """
        account = "S12345"
        date = datetime.datetime.now()
        self.transactions.append(Transaction(date, account, "D", 123.45))
        self.transactions.append(Transaction(date, "C54312", "D", 123.45))
        self.transactions.append(Transaction(date, account, "W", 23.45))
        self.transactions.append(Transaction(date, account, "W", 12))
        self.transactions.append(Transaction(date, "C06789", "D", 3))

        txn_by_account = self.transactions.search(account)
        self.assertEqual(len(txn_by_account), 3)

    def test_save_transactions(self):
        """
        Сохранить реестр транзакций в файл
        """
        account = "C12345"
        date = datetime.datetime.now()
        self.transactions.append(Transaction(date, account, "D", 123.45))
        self.transactions.append(Transaction(date, "S54312", "D", 123.45))
        self.transactions.append(Transaction(date, account, "W", 23.45))
        self.transactions.append(Transaction(date, account, "W", 12))
        self.transactions.append(Transaction(date, "S06789", "D", 3))

        filename = "bank_accounts\\tests\\transactions_tst.dat"
        self.transactions.save(filename)

        self.assertTrue(os.path.isfile(filename))

    def test_load_transactions(self):
        """
        Загрузить реестр из файла и сравнить с первоначальным списком
        """
        account = "S12345"
        date = datetime.datetime.now()
        self.transactions.append(Transaction(date, account, "D", 123.45))
        self.transactions.append(Transaction(date, "C54312", "D", 123.45))
        self.transactions.append(Transaction(date, account, "W", 23.45))
        self.transactions.append(Transaction(date, account, "W", 12))
        self.transactions.append(Transaction(date, "C06789", "D", 3))

        filename = "bank_accounts\\tests\\transactions_tst.dat"
        self.transactions.save(filename)

        loaded = TransactionList.load(filename)
        self.assertEqual(len(loaded), len(self.transactions))

        for idx, txn in enumerate(self.transactions):
            found = loaded[idx]
            self.assertEqual(txn.date, found.date)
            self.assertEqual(txn.txn_type, found.txn_type)
            self.assertEqual(txn.account, found.account)
            self.assertEqual(txn.amount, found.amount)


# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
