# main.py

"""
Система управления банковскими счетами.
Интерфейс командной строки.
"""

import click
import logging

from click import Path
from rich.console import Console

from application import bank_app
from accounts import ACC_TYPE_SAVING, ACC_TYPE_CURRENT

ACCOUNT_TYPE = {
    ACC_TYPE_SAVING: "Saving",
    ACC_TYPE_CURRENT: "Current",
}

console = Console()


@click.command()
@click.argument("account_type", type=click.Choice(list(ACCOUNT_TYPE.keys())), default=ACC_TYPE_SAVING)
@click.argument("balance", type=float, default=0)
@click.option("-n", "--name", prompt="Введите имя пользователя", help="Владелец счета")
def add_account(name: str, account_type: str, balance: float) -> None:
    """
    Добавить новый счет.
    """
    try:
        new_account = bank_app.add_new_account(name, account_type, balance)
        logger.info(f"Создан новый счет #{new_account.account_number}")
        new_account.display()
    except ValueError as error:
        logger.error(f"Ошибка при создании счета: {error}")


@click.command()
@click.argument("account", type=str, required=1)
@click.option("--min_limit", type=float, prompt="Введите минимальный остаток на счете")
@click.option("--max_limit", type=float, prompt="Введите максимальную сумму на счете")
def set_limits(account: str, min_limit: float, max_limit: float) -> None:
    """
    Установить лимиты по счету.
    """
    try:
        changed_account = bank_app.set_limits(account, min_limit, max_limit)
        logger.info(f"Установлены лимиты по счету #:{account}")
        changed_account.display()
    except ValueError as error:
        logger.error(f"Ошибка при установке лимитов по счету #{account}: {error}")


@click.command()
@click.argument("account", type=str, required=1)
@click.option("--amount", type=float, prompt="Введите сумму депозита")
def deposit(account: str, amount: float) -> None:
    """
    Внести сумму на счет.
    """
    try:
        bank_app.deposit(account, amount)
        logger.info(f"Внесен депозит на счет #:{account}")
        found_account = bank_app.get_account(account)
        found_account.display()
    except ValueError as error:
        logger.error(f"Ошибка при внесении средств на счет #{account}: {error}")


@click.command()
@click.argument("account", type=str, required=1)
@click.option("--amount", type=float, prompt="Введите сумму снятия")
def withdraw(account: str, amount: float) -> None:
    """
    Снять сумму со счета.
    """
    try:
        bank_app.withdraw(account, amount)
        logger.info(f"Списана сумма со счета #:{account}")
        found_account = bank_app.get_account(account)
        found_account.display()
    except ValueError as error:
        logger.error(f"Ошибка при списании средств со счета #{account}: {error}")


@click.command()
@click.argument("account", type=str, required=1)
def details(account: str) -> None:
    """
    Отобразить выписку по счету.
    """
    try:
        found_account = bank_app.get_account(account)
        found_account.display_monthly_statement()
    except ValueError as error:
        logger.error(f"Ошибка при отображении счета #{account}: {error}")


@click.command()
@click.argument("filename", type=click.Path(exists=False), required=1)
def export_transactions(filename: Path) -> None:
    """
    Выгрузить историю транзакций в файл.
    """
    try:
        bank_app.save_transactions(filename)
        logger.info(f"История транзакций выгружена в файл: {filename}")
    except ValueError as error:
        logger.error(f"Ошибка при выгрузке транзакций: {error}")


@click.command()
@click.argument("filename", type=click.Path(exists=False), required=1)
def export_accounts(filename: Path) -> None:
    """
    Выгрузить реестр счетов в файл
    """
    try:
        bank_app.save_accounts(filename)
        logger.info(f"История транзакций выгружена в файл: {filename}")
    except ValueError as error:
        logger.error(f"Ошибка при выгрузке транзакций: {error}")


@click.command()
@click.argument("accounts_file", type=click.Path(exists=True), required=1)
@click.argument("transactions_file", type=click.Path(exists=True), required=1)
def import_data(accounts_file: Path, transactions_file: Path) -> None:
    """
    Загрузить счета и транзакции в систему.
    Система будет инициализирована данными из файлов.
    """
    try:
        bank_app.import_data(accounts_file, transactions_file)
        logger.warning(f"Система загружена. Файл счетов: {accounts_file} Файл транзакций:{transactions_file}")
    except ValueError as error:
        logger.error(f"Ошибка при импорте данных: {error}")


@click.command()
def all_accounts() -> None:
    """
    Отобразить все счета в виде списка.
    """
    table = bank_app.get_all_accounts()
    console.print(table)


@click.command()
@click.argument("account", type=str, required=0)
def all_transactions(account: str) -> None:
    """
    Отобразить историю транзакций по счету.
    Если счет не указан - отобразить все транзакции в виде списка.
    """
    try:
        if account is not None:
            found_account = bank_app.get_account(account)
            found_account.display()
        table = bank_app.get_all_transactions(account)
        console.print(table)
    except ValueError as error:
        logger.error(f"Ошибка: {error}")


@click.group
def cli_commands() -> None:
    pass


cli_commands.add_command(add_account)
cli_commands.add_command(set_limits)
cli_commands.add_command(deposit)
cli_commands.add_command(withdraw)
cli_commands.add_command(details)
cli_commands.add_command(export_transactions)
cli_commands.add_command(export_accounts)
cli_commands.add_command(import_data)
cli_commands.add_command(all_accounts)
cli_commands.add_command(all_transactions)


# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('bank.log', encoding="UTF-8")
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

if __name__ == "__main__":
    cli_commands()

