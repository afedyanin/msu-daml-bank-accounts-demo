# Filename: classes.py

class Account:
    ''' суперкласс для банковского счета '''

    def __init__(self, nAccountNo, nCustomerName, nBalance):
        ''' Конструктор '''
        self.__AccountNo = nAccountNo
        self.__CustomerName = nCustomerName
        self.__Balance = nBalance

    def getAccountNo(self):
        ''' получить номер счета '''
        return self.__AccountNo

    def getCustomerName(self):
        ''' получить имя клиента '''
        return self.__CustomerName

    def getBalance(self):
        ''' получить баланс '''
        return self.__Balance

    def setBalance(self, newBalance):
        ''' установить баланс '''
        self.__Balance = newBalance

    def deposit(self, amount):
        ''' внести депозит '''
        self.__Balance = self.__Balance + amount

    def withdraw(self, amount):
        ''' снять деньги '''
        self.__Balance = self.__Balance - amount

    def display(self):
        ''' информация по счету '''
        print("Номер счета:", self.__AccountNo)
        print("Клиент:", self.__CustomerName)
        print("Баланс: ${0:.2f}".format(self.__Balance))


class SavingAccount(Account):  # inheritance
    ''' сохранить '''

    def __init__(self, nAccountNo, nCustomerName, nBalance):
        ''' конструктор '''
        super().__init__(nAccountNo, nCustomerName, nBalance)
        self.__interest = 0.01 / 12

    def display_monthly_statement(self):
        self.setBalance(self.getBalance() * (1 + self.__interest))
        print("Ежемесячная выписка по сберегательному счету ")
        super().display()


class CurrentAccount(Account):
    ''' Аккаунт клиента '''

    def __init__(self, nAccountNo, nCustomerName, nBalance):
        ''' конструктор '''
        super().__init__(nAccountNo, nCustomerName, nBalance)

    def display_monthly_statement(self):
        print("Ежемесячный отчет по текущему счету ")
        super().display()