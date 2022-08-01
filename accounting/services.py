from django.db import transaction as db_transaction
from rest_framework import status
from accounting.exceptions import AtomicAccountTransferException, ZeroAmountError, AccountingEquationError
from accounting.models import Transaction, JournalEntry


@db_transaction.atomic()
def account_transfer(data):
    try:
        if data.je.amount == 0:
            return status.HTTP_400_BAD_REQUEST, {'detail': 'transaction amount should be more than zero'}
        t = Transaction.objects.create(
            type=data.type,
            description=data.description
        )

        cje = JournalEntry.objects.create(account_id=data.je.credit_account,
                                          transaction=t,
                                          amount=data.je.amount,
                                          currency=data.je.currency)
        dje = JournalEntry.objects.create(account_id=data.je.debit_account,
                                          transaction=t,
                                          amount=data.je.amount * -1,
                                          currency=data.je.currency)
    except Exception:
        return status.HTTP_404_NOT_FOUND, {'detail': 'error during transaction creation'}

    if t:
        # try:
        #     t.validate_accounting_equation()
        # except AccountingEquationError:
        #     t.delete()
        #     return status.HTTP_400_BAD_REQUEST, {'detail': 'transaction is not valid'}
        return t
class Balance:
    def __init__(self, balances):
        balance1 = balances[0]
        balance2 = balances[1]

        if balance1['currency'] == 'USD':
            balanceUSD = balance1['sum']
            balanceIQD = balance2['sum']
        else:
            balanceIQD = balance1['sum']
            balanceUSD = balance2['sum']

        self.balanceUSD = balanceUSD
        self.balanceIQD = balanceIQD

    def __add__(self, other):
        self.balanceIQD += other.balanceIQD
        self.balanceUSD += other.balanceUSD
        return [{
            'currency': 'USD',
            'sum': self.balanceUSD
        }, {
            'currency': 'IQD',
            'sum': self.balanceIQD
        }]
def account_balances(account):
    child=account.children_account.all()
    balances=[]
    child_balance=[]
    account_balance=account.balance()
    
    for a in child:
        balance=a.balance()
        child_balance.append(list(balance))


    for j in child_balance:
        for n in j:
            balances.append(n)

    for f in list(account_balance):
        balances.append(f)
 
    if child==[]:
        balances.append(account_balance)
        final=GiveFinalBalance(balances)
    else:
        final= GiveFinalBalance(balances)
    
    print(balances)
    return final

def GiveFinalBalance(balancs):
    balanceUSD=0
    balanceIQD=0
    
    for balance in balancs:
        if balance["currency"]=="USD":
            balanceUSD += balance["sum"]
        else:
            balanceIQD += balance["sum"]
    
    final=[{
        'currency': 'USD',
        'sum': balanceUSD}, {
        'currency': 'IQD',
        'sum': balanceIQD}]
    return final

