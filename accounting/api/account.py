from ninja import Router
from accounting import services
from accounting.models import Account, AccountTypeChoices
from accounting.schemas import AccountOut, FourOFourOut, GeneralLedgerOut
from typing import List
from rest_framework import status


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
    account=Account.objects.get(id=account_id)
    final=services.account_balance(account)
    return status.HTTP_200_OK,{'account':account.name ,'balance':final}


@account_router.get('/account-balances/', response=List[GeneralLedgerOut])
def get_account_balances(request):
    accounts = Account.objects.all()
    result=[]
    for a in accounts:
        final=services.account_balance(a)
        result.append({
            'account':a.name ,'balance':final
        })
    return status.HTTP_200_OK,result

class Balance:
    def __init__(self, balances):
        balance1 = balances[0]
        balance2 = balances[1]

        if balance1['currency'] == 'USD':
            balanceUSD = balance1['sum']
            balanceIQD = balance2['sum']
        else:
            balanceIQD = balance1['sum']
            balanceUSD = balance2['sum']

        self.balanceUSD = balanceUSD
        self.balanceIQD = balanceIQD

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
        
def greater(self, other):
    print(self.balanceUSD > other.balanceUSD,self.balanceIQD > other.balanceIQD) 

def lesser(self, other):
    print(self.balanceUSD < other.balanceUSD,self.balanceIQD < other.balanceIQD)


def is_zero(self):
    if self.balanceIQD == 0 and self.balanceUSD == 0:
        return True
    else:
        return False