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




def get_balance(balances):
    IQD_balance=0
    USD_balance=0
    
    
    for a in balances:
        if (a['currency'] == 'IQD'):
            IQD_balance += a['total'] 
        else:
            USD_balance += a['total']

    total_balance = [{'currency':"USD", 'total':USD_balance},{'currency':'IQD', 'total':IQD_balance}]
    return total_balance