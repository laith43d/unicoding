from asyncio.windows_events import NULL
from decimal import Decimal
from importlib.abc import PathEntryFinder
from typing_extensions import Self
from django.http import Http404, HttpRequest
from ninja import Router
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from accounting.models import Account, AccountTypeChoices
from accounting.schemas import AccountOut, FourOFourOut, GeneralLedgerOut
from typing import List, final
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
        account = Account.objects.get(id=account_id)
        return account
    except Account.DoesNotExist:
        return 404, {'detail': f'Account with id {account_id} does not exist'}


@account_router.get('/get_account_types/')
def get_account_types(request):
    return {t[0]: t[1] for t in AccountTypeChoices.choices}


@account_router.get('/account-balance/{account_id}', response=GeneralLedgerOut)
def get_account_balance(request, account_id: int):
    account = get_object_or_404(Account, id=account_id)

    balance = account.balance()

    journal_entries = account.journal_entries.all()

    return 200, {'account': account.name, 'balance': list(balance), 'jes': list(journal_entries)}


@account_router.get('/account-balances/', response=List[GeneralLedgerOut])
def get_account_balances(request):
    accounts = Account.objects.all()
    result = []

    for a in accounts:
        result.append({
            'account': a.name, 'balance': list(a.balance()),'id':a.id
        }) 
        
    for b in accounts:
        if b.parent_id == None:
            result[next((i for i, x in enumerate(result) if x["id"] == b.id))]['balance'] = (Balance.__add__(Balance(result[next((i for i, x in enumerate(result) if x["id"] == b.id))]['balance']), Balance(list(b.balance()))))
        else:
            result[next((i for i, x in enumerate(result) if x["id"] == b.parent_id))]['balance'] = (Balance.__add__(Balance(result[next((i for i, x in enumerate(result) if x["id"] == b.parent_id))]['balance']), Balance(list(b.balance()))))  

    return status.HTTP_200_OK, result


class Balance:
    def __init__(self, balances):
        balanceIQD = []
        balanceUSD = []
        for i in balances:
            if i['currency'] == 'USD':
                balanceUSD.append(int(i['sum']))
            if i['currency'] == 'IQD':
                balanceIQD.append(int(i['sum']))    

        self.balanceUSD = sum(balanceUSD)
        self.balanceIQD = sum(balanceIQD)

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