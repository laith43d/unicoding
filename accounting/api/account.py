from ninja import Router
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from accounting.models import Account, AccountTypeChoices
from accounting.schemas import AccountOut, FourOFourOut, GeneralLedgerOut, GeneralLedgerOutBalances
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

    parent_list = Account.objects.filter(parent_id__isnull=False).values_list('parent', flat=True)

    if account_id in parent_list:
        balance = account.parent_balance()
    else:
        balance = account.balance()

    journal_entries = account.journal_entries.all()

    return 200, {'account': account.name, 'balance': list(balance), 'jes': list(journal_entries)}


@account_router.get('/account-balances/', response=List[GeneralLedgerOutBalances])
def get_account_balances(request):
    accounts = Account.objects.all()
    result = []
 
    parent_list = Account.objects.filter(parent_id__isnull=False).values_list('parent',flat=True)
    
    for a in accounts:
        if a.id in parent_list:
            result.append({
                'account': a.name, 
                'balance': list( a.parent_balance() ),
                'parent_id':a.parent_id ,
                'id':a.id 
            }) 
        
        result.append({
            'account': a.name, 
            'balance': list( a.balance() ),
            'parent_id':a.parent_id , 
            'id':a.id 
        }) 
         
    return status.HTTP_200_OK, result
