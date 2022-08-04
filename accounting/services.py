from django.db import transaction as db_transaction
from rest_framework import status
from accounting.exceptions import AtomicAccountTransferException, ZeroAmountError, AccountingEquationError
from accounting.models import Account, Balance, Transaction, JournalEntry


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

#Task 3 Service Function ✍️(◔◡◔) ↓↓↓↓↓↓↓↓↓↓↓↓

def get_balance_by_id(id):
    try:
        account = Account.objects.get(id = id)
        total_balance = Balance(account.balance())
        print(account.balance(), 13123123)
        print('----------------')
        print(total_balance.balanceIQD)
        x = account
        children_ids = []
        while 1:
            try:
                x = x.child.all()
                for x in x:
                    if x.id:
                        children_ids.append(x.id)
                        if x:
                            balance_x = Balance(x.balance())
                            total_balance.__add__(balance_x)
                    else: break
            except: break
        return [[{
            'currency': 'USD',
            'sum': f'{total_balance.balanceUSD}'
        }, {
            'currency': 'IQD',
            'sum': f'{total_balance.balanceIQD}'
        }], account.name, children_ids]
    except: return None