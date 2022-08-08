from http import HTTPStatus
from ninja import Router
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from accounting.models import Account, AccountTypeChoices
from accounting.schemas import AccountOut, FourOFourOut, GeneralLedgerOut
from typing import List
from django.db.models import Sum, Avg
from accounting.services import get_balance

from restauth.authorization import AuthBearer

account_router = Router(tags=['account'])


@account_router.get("/get_all", response=List[AccountOut])
def get_all(request):
    return HTTPStatus.OK, Account.objects.order_by('full_code')


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

    return HTTPStatus.OK, {'account': account.name, 'balance': list(balance), 'jes': list(journal_entries)}


#this end-point for task solution(get all balances)
@account_router.get('/account-balances/') 
def get_account_balances(request):
    accounts = Account.objects.all()
    result=[]
    for a in accounts:
        jes = a.journal_entries.all()
        name = a.name
        children_accounts = a.children.all()
        balance =[]
        children_balances=[]
        account_balance = a.balance()

        if list(jes) == []:
            final_balance = 0
            result.append({'account': name,'balance': final_balance })
        else:
            for a in children_accounts:
                balance.append(list(a.balance()))
    
            for a in balance:
                for i in a:
                    children_balances.append(i)
    

            child_balance = Balance(get_balance(children_balances))
            parent_balance= Balance(account_balance)

            if list(children_accounts) != []:
                final_balance = child_balance.__add__(parent_balance)
            else:
                final_balance = list(account_balance)
        
            result.append({'account': name,'balance': final_balance })
    return HTTPStatus.OK, result



#this end-point for task solution(get balance for specific account)
@account_router.get('/account-balance/{account_id}')
def get_account_balance(request, account_id: int):
    account = get_object_or_404(Account, id=account_id)
    children_accounts = account.children.all()
    balance =[]
    children_balances=[]
    
    for a in children_accounts:
            balance.append(list(a.balance()))
    
    for a in balance:
        for i in a:
            children_balances.append(i)
    
    child_balance = Balance(get_balance(children_balances))
    parent_balance= Balance(account.balance())

    if list(children_accounts) != []:
        print(children_accounts)
        final_balance = child_balance.__add__(parent_balance)
    else:
        final_balance = list(account.balance())
    
    return HTTPStatus.OK, {'account': account.name ,'balance': final_balance }

#class balance
class Balance:

    def __init__(self, balances):
       
        balanceIQD = 0
        balanceUSD = 0
        for i in balances:
            if i['currency'] == 'USD':
                balanceUSD = i['sum']
            if i['currency'] == 'IQD':
                balanceIQD = i['sum']

       
        self.balanceUSD = balanceUSD
        self.balanceIQD = balanceIQD

    def __add__(self, other):
        
        self.balanceIQD += other.balanceIQD
        self.balanceUSD += other.balanceUSD
        result=[{
            'currency': 'USD',
            'sum': self.balanceUSD
        }, {
            'currency': 'IQD',
            'sum': self.balanceIQD
        }]

        return result