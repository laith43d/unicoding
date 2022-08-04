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



# perfectionism
class Balance:
    def __init__(self, balances:list[list[dict]]):
        listOfInfo = [item for sublist in balances for item in sublist]
        currency_info = [c['currency'] for c in listOfInfo]
        currency_info =  list(dict.fromkeys(currency_info))

        usd_amount = 0
        iqd_amount = 0

        currency_amount = {}
        currency_balance = {}
        currency_balance_list = []
        for c in currency_info:
            currency_amount.update({c:list(filter(lambda currency: currency['currency'] == c, listOfInfo))})
        # print(currency_amount)
        for k,v in currency_amount.items():
            currency_balance = ({
            'currency': k,
            'sum': sum([i['sum'] for i in v])
        })
            currency_balance_list.append(currency_balance)
            
        for d in currency_balance_list:
            if d['currency'] == "USD":
                usd_amount = d['sum']
                
            elif d['currency'] == "IQD":
                iqd_amount = d['sum']
                
        self.balanceUSD = usd_amount
        self.balanceIQD = iqd_amount
        self.currency_balance_list = currency_balance_list
    def sinsOfTheFather(self):
        return self.currency_balance_list
    def __gt__(self,other):
        whichCurrencyBigger = []
        if self.balanceUSD > other.balanceUSD:
            whichCurrencyBigger.append(True)
        else:
            whichCurrencyBigger.append(False)
            
        if self.balanceIQD > other.balanceIQD:
            whichCurrencyBigger.append(True)
        else:
            whichCurrencyBigger.append(False)
            
            return whichCurrencyBigger
    def isZero(self):
        if not self.balanceUSD and not self.balanceIQD:
            return True
        return False
        
# b1 = Balance([[{'currency': 'USD', 'sum': Decimal('6000')},{'currency': 'IQD', 'sum': Decimal('6000000')}]])
# b2 = Balance([[{'currency': 'USD', 'sum': Decimal('6000')}]])
# print(b1 > b2)
# b3 = Balance([[{'currency': 'USD', 'sum': Decimal('0')}]])
# print(b3.isZero())
    
@account_router.get('/account-balances/', response=List[GeneralLedgerOut])
def get_account_balances(request):
    accounts = Account.objects.all()
    transactions = Transaction.objects.all()
    result = []
    d={}
    father =[]
    father_id =[]
    counter = 0

    for a in accounts:
        result.append({
            'account': a.name,
            'balance': list(a.balance()),
            # 'jes':list(a.journal_entries.all())
        })
        
        if a.children.all():
            father.append(a.name)
            # print(father)
            father_id.append(a.id)
            fatherInfo =({father_id[counter]:father[counter]})
            counter += 1
            sinsOFtheChild = [i.balance() for i in a.children.all()]
            # d["{0}".format([i['parent_id'] for i in a.children.values()][0])] = sinsOFtheChild
            d["{0}".format([fatherInfo[i['parent_id']] for i in a.children.values()][0])] = sinsOFtheChild
    for r in result:
        for k,v in d.items():
            if r['account'] == k:
                b = Balance(v)
                print(v)
                r['balance'] = b.sinsOfTheFather()
                
    return status.HTTP_200_OK, result


# this code is greate but not the best
# @account_router.get('/account-balances/', response=List[GeneralLedgerOut])
# def get_account_balances(request):
#     accounts = Account.objects.all()
#     transactions = Transaction.objects.all()
#     result = []
#     d={}
#     father =[]
#     father_id =[]
#     counter = 0
#     dd1={}
#     for a in accounts:
#         result.append({
#             'account': a.name,
#             'balance': list(a.balance()),
#             # 'jes':list(a.journal_entries.all())
#         })
        
#         if a.children.all():
#             father.append(a.name)
#             # print(father)
#             father_id.append(a.id)
#             fatherInfo =({father_id[counter]:father[counter]})
#             counter += 1
#             sinsOFtheChild = [i.balance() for i in a.children.all()]
#             # d["{0}".format([i['parent_id'] for i in a.children.values()][0])] = sinsOFtheChild
#             d["{0}".format([fatherInfo[i['parent_id']] for i in a.children.values()][0])] = sinsOFtheChild
#     for r in result:
#         for k,v in d.items():
#             if r['account'] == k:
#                 b = Balance(v)
#                 print(b.sinsOfTheFather())
#                 r['balance'] = b.sinsOfTheFather()
    
#     balances = {}
#     for x in range(len(list(d.keys()))):
#         Balance_USD=0
#         Balance_IQD=0
#         l = d[list(d.keys())[x]]
        
#         flat_list = [item for sublist in l for item in sublist]
        
#         for z in flat_list:
#             final_balance =[]
#             if z['currency'] == "USD":
#                 Balance_USD += z['sum']
#                 dd1 = ({"currency":z['currency'],"sum":Balance_USD})
#             elif z['currency'] == "IQD":
#                 Balance_IQD += z['sum']
#                 dd2 = ({"currency":z['currency'],"sum":Balance_IQD})
            
#         final_balance = [dd1,dd2]
#         balances.update({father[x]:final_balance})
#     for r in result:
#         for k,v in balances.items():
#             if r['account'] == k:
#                 r['balance'] = v         
#     return status.HTTP_200_OK, result

    # the code below was written by a sicopath not recomended to read it or even use it
    # child ={}
    # father=[]
    # data = collections.defaultdict(list)
    # dd={}
    # balances = []
    # for i in accounts.values():
    #     if i['parent_id'] == None:father.append(i['name'])
    #     else:child.update({i['name']:i['parent_id']})
    # combo = {'|'.join(sorted(k for k in child.keys() if child[k] == v)): v for v in set(child.values())}
    # for z in range(len(result)):
    #     for j in range(len(list(combo.items()))):
    #         if result[z]['account'] in list(combo.items())[j][0].split('|'):
    #             f = [f"{i['currency']}|{i['sum']}" for i in result[z]['balance']]
    #             data[repr(list(combo.items())[j][0].split('|'))].append(f)
    # numOfFathers =0
    # for k,o in data.items():
    #     l = [i.split("|") for i in list(itertools.chain(*data[k]))]
    #     currency = [z[0] if z[0] =="USD" else "IQD" for z in l]
    #     money = [z[1] for z in l]
    #     # dd.update({"USD Amount":0,"IQD Amount":0})
    #     usdMoney,iqdMoney =0,0
    #     for z in range(len(money)):
    #         if currency[z] == "USD":
    #             usdMoney += int(money[z])
    #             dd = ({"children":k,"USD Amount":usdMoney,"IQD Amount":iqdMoney})
    #         elif currency[z] == "IQD":
    #             iqdMoney += int(money[z])
    #             dd = ({"children":k,"USD Amount":usdMoney,"IQD Amount":iqdMoney})
    #     dd.update({"father":father[numOfFathers]})
    #     balances.append(dd) 
    #     numOfFathers = numOfFathers+ 1   

# php is not a bad language but django is great
    
    # for c in range(len(result)):
    #     for h in balances:
    #         if result[c]['account'] == h['father']:
    #             result[c]['balance'].extend([{"currency":"USD","sum":h["USD Amount"]},
    #             {"currency":"IQD","sum":h["IQD Amount"]}])

