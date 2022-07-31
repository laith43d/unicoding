from decimal import Decimal
from unicodedata import decimal, name
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
        if len(a.children.all()) > 0:
            lisT_children = a.children.values('name')
            temp_balance = [{'currency': 'IQD', 'sum': Decimal(0)},{'currency': 'USD', 'sum': Decimal(0)}]
            if len(a.journal_entries.all()) > 0:
                temp_balance = Balance(temp_balance) + Balance(a.balance())
            for i in lisT_children:
                s = Account.objects.get(name = i['name'])
                b = s.balance()
                temp_balance = Balance(temp_balance) + Balance(b)
            result.append({'account': a.name, 'balance': temp_balance})
        else:
            temp_balance = [{'currency': 'IQD', 'sum': Decimal(0)},{'currency': 'USD', 'sum': Decimal(0)}]
            temp_balance = Balance(temp_balance) + Balance(a.balance())
            result.append({'account': a.name, 'balance': temp_balance})
    return status.HTTP_200_OK, result




class Balance:
    def __init__(self, balances):
        if len(balances) == 2 :
            balance1 = balances[0]
            balance2 = balances[1]

            if balance1['currency'] == 'USD':
                balanceUSD = balance1['sum']
                balanceIQD = balance2['sum']
            else:
                balanceIQD = balance1['sum']
                balanceUSD = balance2['sum']
        elif len(balances) == 1:
            balance1 = balances[0]
            if balance1['currency'] == 'USD':
                balanceUSD = balance1['sum']
                balanceIQD = 0
            else:
                balanceIQD = balance1['sum']
                balanceUSD = 0
        else:
            balanceUSD = 0
            balanceIQD = 0
        self.balanceUSD = balanceUSD
        self.balanceIQD = balanceIQD  
    def __add__(self, other):
        self.balanceIQD += other.balanceIQD
        self.balanceUSD += other.balanceUSD
        return [{
            'currency': 'IQD',
            'sum': self.balanceIQD
        }, {
            'currency': 'USD',
            'sum': self.balanceUSD
        }]

