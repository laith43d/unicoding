from asyncio.windows_events import NULL
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
    if bool(account.children.all()) is True:
        balance_parant = Balance(balances=list(balance))
        childern_balances = []
        for i in account.children.all():
                childern_balances.append(list(i.balance()))
                
        childern_balance_objs = []
        for i in childern_balances:
            childern_balance_objs.append(Balance(balances=list(i)))
        
        for i in childern_balance_objs:
            balance_parant.__add__(i)
        
        balance = [{'currency': 'USD', 'sum': balance_parant.balanceUSD},{'currency': 'IQD', 'sum': balance_parant.balanceIQD}]
        
        
    
    
    journal_entries = account.journal_entries.all()

    return 200, {'account': account.name, 'balance': list(balance), 'jes': list(journal_entries)}


@account_router.get('/account-balances/', response=List[GeneralLedgerOut])
def get_account_balances(request):
    accounts = Account.objects.all()
    
    result = []
    for a in accounts:
        balance = a.balance()
        if bool(a.children.all()) is True:
            balance_parant = Balance(balances=list(balance))
            childern_balances = []
            for i in a.children.all():
                    childern_balances.append(list(i.balance()))

            childern_balance_objs = []
            for i in childern_balances:
                childern_balance_objs.append(Balance(balances=list(i)))

            for i in childern_balance_objs:
                balance_parant.__add__(i)
        
            balance = [{'currency': 'USD', 'sum': balance_parant.balanceUSD},{'currency': 'IQD', 'sum': balance_parant.balanceIQD}]
        
        result.append({
            'account': a.name, 'balance': list(balance)
        })

    return status.HTTP_200_OK, result



class Balance:
    def __init__(self, balances):
        if len(balances) == 2:
            balance1 = (balances[0])
            balance2 = (balances[1])

            if balance1['currency'] == 'USD':
                balanceUSD = balance1['sum']
                balanceIQD = balance2['sum']
            else:
                balanceIQD = balance1['sum']
                balanceUSD = balance2['sum']

            self.balanceUSD = balanceUSD
            self.balanceIQD = balanceIQD

        elif len(balances) == 1:
            balance = (balances[0])
            if balance['currency'] == 'USD':
                self.balanceUSD = balance['sum']
                self.balanceIQD = 0
                
            else:
                self.balanceUSD = 0
                self.balanceIQD = balance['sum']
                
        else:
            self.balanceUSD = 0
            self.balanceIQD = 0
    
    def __init__(self, amount1, currency1, amount2, currency2):
        if currency1 == 'USD':
            self.balanceUSD = amount1
            self.balanceIQD = amount2
        elif currency1 == 'IQD':
            self.balanceUSD = amount2
            self.balanceIQD = amount1
            

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
    
    def __lt__(self, other):
        iqd = self.balanceIQD < other.balanceIQD
        usd = self.balanceUSD < other.balanceUSD
        return(f'({usd},{iqd})')
        
    def __gt__(self, other):
        iqd = self.balanceIQD > other.balanceIQD
        usd = self.balanceUSD > other.balanceUSD
        return(f'({usd},{iqd})')
    
    def isZero(self):
        if self.balanceIQD == 0 and self.balanceUSD == 0:
            return True
        else:
            return False