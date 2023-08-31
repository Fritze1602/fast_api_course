import pytest
from app.calculations import add, multiply, divide, subtract, BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def initvalue_bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("a,b, expected", [
    (3, 2, 5), (7, 1, 8), (4, -2, 2)
])
def test_add(a, b, expected):
    assert add(a, b) == expected


def test_subtract():
    assert subtract(5, 2) == 3


def test_multiply():
    assert multiply(2, 5) == 10


def test_divide():
    assert divide(10, 2) == 5


def test_bank_set_initial_amount(initvalue_bank_account):

    assert initvalue_bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_bank_withdraw(initvalue_bank_account):
    initvalue_bank_account.withdraw(30)
    assert initvalue_bank_account.balance == 20


def test_bank_deposit(initvalue_bank_account):
    initvalue_bank_account.deposit(20)
    assert initvalue_bank_account.balance == 70


def test_bank_collect_interest(initvalue_bank_account):
    initvalue_bank_account.collect_interest()
    assert round(initvalue_bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposited,withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000),
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

# Testing expected Failes -> Exception


def test_insufficient_funds(initvalue_bank_account):
    with pytest.raises(InsufficientFunds):
        initvalue_bank_account.withdraw(500)
