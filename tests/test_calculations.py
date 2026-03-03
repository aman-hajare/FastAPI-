from app.calculations import add, subtract, multiply, divde, BankAccount, InsufficientFunds
import pytest

# function,file,folder,__init__.py file and naming metter use test_...like this and same file name as define func inside app or testing like this  test\ test.<filename>.py and run command as a module if normal show module error like python -m tests.calculations  
## ---------- ##
@pytest.mark.parametrize("x, y, result",[
    (3, 2, 5),
    (3, 3, 6),
    (5, 5, 10)
])
def test_add(x,y,result):
    # print("testing add function")
    assert add(x,y) == result
    # assert add(5, 3) == 8
# test_add()

def test_subtract():
    assert subtract(10, 3) == 7
test_subtract()

def test_multiply():
    assert multiply(4, 3) == 12
test_multiply()

def test_divde():
    assert divde(10, 2) == 5
test_divde()

## ---------- ##

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

def test_bank_set_initial_amount(bank_account):
    # bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    # bank_account = BankAccount()
    assert zero_bank_account.balance == 0

def test_deposit(bank_account):
    # bank_account = BankAccount(50)   
    bank_account.deposit(20) 
    assert bank_account.balance == 70
    
def test_withdraw(bank_account):
    # bank_account = BankAccount(50) 
    bank_account.withdraw(20) 
    assert bank_account.balance == 30

def test_collect_interest(bank_account):
    # bank_account = BankAccount(50)
    bank_account.collect_intrest()
    assert round(bank_account.balance) == 55

@pytest.mark.parametrize ("depositX, withdrawY, amountR",[
    (50, 10, 40),
    (400, 100, 300),
    (1200,200, 1000),
])
def test_bank_transaction(zero_bank_account, depositX, withdrawY, amountR):
    zero_bank_account.deposit(depositX)    
    zero_bank_account.withdraw(withdrawY)
    assert zero_bank_account.balance == amountR

def test_insffucient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)