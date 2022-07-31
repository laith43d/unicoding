from ninja import Router
from django.shortcuts import get_object_or_404
from accounting.models import Account, AccountTypeChoices
from accounting.schemas import AccountOut, FourOFourOut, GeneralLedgerOut
from typing import List
from rest_framework import status
from accounting.services import get_balance


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


@account_router.get('/account-balance/') 
def account_balance(request, ID: int):
    account = Account.objects.get(id=ID)
    childrenAccounts = account.children.all()
    account_balance = account.balance()
    children_balances=[]
    balances=[]

    for a in childrenAccounts:
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
        final_balance= list(account_balance)

    return status.HTTP_200_OK, {'account': account.name, 'balance':final_balance}

