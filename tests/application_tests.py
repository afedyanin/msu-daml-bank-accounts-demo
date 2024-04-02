# application_tests.py

"""
Тест кейсы основных бизнес сценариев.
"""

import unittest
from unittest import TestCase

from bank_accounts.application import bank_app


class TestApplication(TestCase):
    def test_accounts_loaded(self):
        accounts_table = bank_app.get_all_accounts()
        self.assertTrue(len(accounts_table.rows) > 0)


# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
