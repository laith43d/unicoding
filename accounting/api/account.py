from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from rest_framework import status
from accounting.models import  Account
from accounting.schemas import GeneralLedgerOut


account_router = Router(tags=['account'])


"""@account_router.get("/get_all", response=List[AccountOut])
def get_all(request):
    return status.HTTP_200_OK, accounting.models.Account.objects.order_by('full_code')

"""
"""@account_router.get('/get_one/{account_id}/', response={
    200: AccountOut,
    404: FourOFourOut,
})
def get_one(request, account_id: int):
    try:
        from accounting.models import Account
        account = Account.objects.get(id=account_id)
        return account
    except Account.DoesNotExist:
        return 404, {'detail': f'Account with id {account_id} does not exist'}

"""
"""@account_router.get('/get_account_types/')
def get_account_types(request):
    return {t[0]: t[1] for t in AccountTypeChoices.choices}
"""

@account_router.get('/account-balance/{account_id}', response=GeneralLedgerOut)
def get_account_balance(request, account_id: int):
    account = get_object_or_404(Account, id=account_id)

    balance = account.balance()

    journal_entries = account.journal_entries.all()

    return 200, {'account': account.name, 'balance': list(balance), 'jes': list(journal_entries)}


@account_router.get('/account-balances/', response=List[GeneralLedgerOut])
def get_account_balances(request):
    account = Account.objects.all()
    result = []
    for a in account:
        result.append({
            'account': a.name, 'balance': list(a.balance())
        })
    return status.HTTP_200_OK, result

@account_router.get('/total_balance/', response=GeneralLedgerOut)
def get_totals_balance(request):
    account = Account.objects.all()
    total__total_balance = []
    for to in account:
        total__total_balance.append({'account': to.name, 'balance': list(to.total_balance())})
    return 200, total__total_balance



