from ninja import Router
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from accounting.models import Account, AccountTypeChoices,Balance
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
        result.append({
            'account': a.name, 'balance': list(a.balance())
        })

    return status.HTTP_200_OK, result

@account_router.get('/total_balance/', response=List[GeneralLedgerOut])
def get_total_balance(request, account_id: int):

    account = Account.objects.get(id=account_id)
    children = account.children.all()
    balances = []
    if  account.children.all() == []: 
        total_balance = account.balance()

    else:
        parent_balance = account.balance()

        for child in children:
            balances = [child.balance()]

            balance1 = balances[0]
            balance2 = balances[1]


        total_balance =  Balance(parent_balance) + Balance(balance1) + Balance(balance2)


    return total_balance
