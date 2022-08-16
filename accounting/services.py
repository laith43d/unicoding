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
    
    
    
 def __gt__(self, other):

        if self.balanceUSD > other.balanceUSD :
            StaUSD = True
        else:
            StaUSD = False
        if self.balanceIQD > other.balanceIQD :
            StaIQD = True
        else:
            StaIQD = False
        return {'USD':StaUSD},{'IQD':StaIQD}


    def __lt__(self,other):

        if self.balanceUSD < other.balanceUSD :
            StaUSD = True
        else:
            StaUSD = False
        if self.balanceIQD < other.balanceIQD :
            StaIQD = True
        else:
            StaIQD = False
        return {'USD':StaUSD},{'IQD':StaIQD}

    def is_zero(self):
        if self.balanceIQD == 0 and self.balanceUSD == 0 :
            return True
        else:
            return False

