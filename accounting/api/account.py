from ninja import Router
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from accounting.models import Account, AccountTypeChoices
from accounting.schemas import AccountOut, FourOFourOut, GeneralLedgerOut
from typing import List
from django.db.models import Sum, Avg
from rest_framework import status

from restauth.authorization import AuthBearer

account_router = Router(tags=['account'])


@account_router.get("/get_all", response=List[AccountOut])
def get_all(request):
    return status.HTTP_200_OK, Account.objects.order_by('full_code')


@account_router.get('/get_one/{account_id}/', response={
    200: AccountOut,
    404: FourOFourOut,
})
def get_one(request, account_id: int):
    try:
        return Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': f'Account with id {account_id} does not exist'}


@account_router.get('/get_account_types/')
def get_account_types(request):
    return {t[0]: t[1] for t in AccountTypeChoices.choices}


@account_router.get('/account-balance/{account_id}', response=GeneralLedgerOut)
def get_account_balance(request, account_id: int):
    global balance, balanceUSD
    account = get_object_or_404(Account, id=account_id)
    if account.parent is None:
        balance=account.parent_balances

    else:
        balance = account.balance()
    journal_entries = account.journal_entries.all()
    return 200, {'account': account.name, 'balance': list(balance), 'jes': list(journal_entries)}


@account_router.get('/account-balances/', response=List[GeneralLedgerOut])
def get_account_balances(request):
    accounts = Account.objects.all()
    result = [
        {'account': a.name, 'balance': list(a.balance())} for a in accounts
    ]
    return status.HTTP_200_OK, result


