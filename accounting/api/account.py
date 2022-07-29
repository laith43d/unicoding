import collections
from decimal import Decimal
from locale import currency
from unicodedata import name
from ninja import Router
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from accounting.models import Account, AccountTypeChoices, Transaction
from accounting.schemas import AccountOut, FourOFourOut, GeneralLedgerOut
from typing import Counter, List
import itertools
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
    transactions = Transaction.objects.all()
    result = []
    for a in accounts:
        result.append({
            'account': a.name,
            'balance': list(a.balance()),
            # 'jes':list(a.journal_entries.all())
        })
    child ={}
    father=[]
    data = collections.defaultdict(list)
    dd={}
    balances = []
    for i in accounts.values():
        if i['parent_id'] == None:father.append(i['name'])
        else:child.update({i['name']:i['parent_id']})
    combo = {'|'.join(sorted(k for k in child.keys() if child[k] == v)): v for v in set(child.values())}
    for z in range(len(result)):
        for j in range(len(list(combo.items()))):
            if result[z]['account'] in list(combo.items())[j][0].split('|'):
                f = [f"{i['currency']}|{i['sum']}" for i in result[z]['balance']]
                data[repr(list(combo.items())[j][0].split('|'))].append(f)
    numOfFathers =0
    for k,o in data.items():
        l = [i.split("|") for i in list(itertools.chain(*data[k]))]
        currency = [z[0] if z[0] =="USD" else "IQD" for z in l]
        money = [z[1] for z in l]
        # dd.update({"USD Amount":0,"IQD Amount":0})
        usdMoney,iqdMoney =0,0
        for z in range(len(money)):
            if currency[z] == "USD":
                usdMoney += int(money[z])
                dd = ({"children":k,"USD Amount":usdMoney,"IQD Amount":iqdMoney})
            elif currency[z] == "IQD":
                iqdMoney += int(money[z])
                dd = ({"children":k,"USD Amount":usdMoney,"IQD Amount":iqdMoney})
        dd.update({"father":father[numOfFathers]})
        balances.append(dd) 
        numOfFathers = numOfFathers+ 1   

    
    for c in range(len(result)):
        for h in balances:
            if result[c]['account'] == h['father']:
                result[c]['balance'].extend([{"currency":"USD","sum":h["USD Amount"]},{"currency":"IQD","sum":h["IQD Amount"]}])
    
    return status.HTTP_200_OK, result



