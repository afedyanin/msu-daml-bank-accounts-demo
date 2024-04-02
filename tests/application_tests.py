# application_tests.py

"""
Тест кейсы основных бизнес сценариев.
"""

import unittest
from unittest import TestCase

from bank_accounts.application import bank_app


class TestApplication(TestCase):
    def test_accounts_loaded(self):
        self.assertTrue(len(bank_app.accounts) > 0)

    def test_transactions_loaded(self):
        self.assertTrue(len(bank_app.transactions) > 0)


# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
