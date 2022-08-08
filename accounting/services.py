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
        
def account_balance(account):
    child=account.children_account.all()
    balances=[]
    child_balance=[]
    account_balance=account.balance() 
    for i in child:
        balance=i.balance()
        child_balance.append(list(balance))


    for f in child_balance:
        for j in f:
            balances.append(j)

    for n in list(account_balance):
       balances.append(n)
 
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

