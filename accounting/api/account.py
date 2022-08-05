from ninja import Router
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from accounting.models import Account, AccountTypeChoices
from accounting.schemas import AccountOut, FourOFourOut, GeneralLedgerOut
from typing import List
from django.db.models import Sum, Avg
from http import HTTPStatus

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
    account = Account.objects.get(id=account_id)
    children_accounts = account.children.all()
    account_balance = account.balance()
    children_balances=[]
    balances=[]

    for a in children_accounts:
        balance = a.balance()
        children_balances.append(list(balance))

    for a in children_balances:
        for i in a:
            balances.append(i)

    for a in list(account_balance):
        balances.append(a)

    if account.parent == None:
        final_balance= get_balance(balances)
    else:
        final_balance=list(children_balances)+list(account_balance)

    return HTTPStatus.OK, {'account': account.name, 'balance':final_balance}



def get_balance(balances):
    IQD_balance=0
    USD_balance=0
    for a in balances:
        if a['currency'] == 'IQD':
            IQD_balance += a['sum'] 
        else:
            USD_balance += a['sum']

    final_balance = [{'currency':'USD', 'sum':USD_balance},{'currency':'IQD', 'sum':IQD_balance}]
    return final_balance
    