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


'''@account_router.get('/account-balance/{account_id}', response=GeneralLedgerOut)
def get_account_balance(request, account_id: int):
    account = get_object_or_404(Account, id=account_id)
    balance = account.balance()

    journal_entries = account.journal_entries.all()

    return 200, {'account': account.name, 'balance': list(balance), 'jes': list(journal_entries)}'''


@account_router.get('/account-balances/', response=List[GeneralLedgerOut])
def get_account_balances(request):
    accounts = Account.objects.all()
    result = []
    for a in accounts:
        result.append({
            'account': a.name, 'balance': list(a.balance())
        })

    return status.HTTP_200_OK, result


class Balance:

    def __init__(self, balances):
        balance1 = balances[0]
        balance2 = balances[1]
        if balance1['currency'] == 'USD':
            balanceUSD = balance1['amount']
            balanceIQD = balance2['amount']
        else:
            balanceIQD = balance1['amount']
            balanceUSD = balance2['amount']
        self.balanceUSD = balanceUSD
        self.balanceIQD = balanceIQD

    def __add__(self, other):
        self.balanceIQD += other.balanceIQD
        self.balanceUSD += other.balanceUSD
        return [{
            'currency': 'USD',
            'amount': self.balanceUSD
        }, {
            'currency': 'IQD',
            'amount': self.balanceIQD
        }]

    # task 4:
    def __gt__(self, other):
        if self.balanceUSD > other.balanceUSD and self.balanceIQD > other.balanceIQD:
            return [{'USD': True}, {'IQD': True}]
        elif self.balanceUSD < other.balanceUSD and self.balanceIQD < other.balanceIQD:
            return [{'USD': False}, {'IQD': False}]
        elif self.balanceUSD < other.balanceUSD and self.balanceIQD > other.balanceIQD:
            return [{'USD': False}, {'IQD': True}]
        elif self.balanceUSD > other.balanceUSD and self.balanceIQD < other.balanceIQD:
            return [{'USD': True}, {'IQD': False}]
        else:
            return 'try again, one or both currency are equal'

    def __lt__(self, other):
        if self.balanceUSD < other.balanceUSD and self.balanceIQD < other.balanceIQD:
            print([{'USD': True}, {'IQD': True}])
        elif self.balanceUSD > other.balanceUSD and self.balanceIQD > other.balanceIQD:
            return [{'USD': False}, {'IQD': False}]
        elif self.balanceUSD > other.balanceUSD and self.balanceIQD < other.balanceIQD:
            return [{'USD': False}, {'IQD': True}]
        elif self.balanceUSD < other.balanceUSD and self.balanceIQD > other.balanceIQD:
            return [{'USD': True}, {'IQD': False}]
        else:
            return 'try again, one or both currency are equal'

    def is_zero(self):
        if self.balanceUSD == 0 and self.balanceIQD == 0:
            print(True)
        else:
            print(False)


'''class Balance:

    def init(self, balances):
        if balances.index == 1:  # when the account have two currencies
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

        elif not balances:  # when the account contains no currency
            self.balanceUSD = 0
            self.balanceIQD = 0

        elif balances.index == 0:  # when the account have one currency
            balance = balances[0]

            if balance['currency'] == 'USD':
                balanceUSD = balance['sum']
                balanceIQD = 0
            else:
                balanceIQD = balance['sum']
                balanceUSD = 0
            self.balanceUSD = balanceUSD
            self.balanceIQD = balanceIQD

    def add(self, other):
        self.balanceIQD += other.balanceIQD
        self.balanceUSD += other.balanceUSD
        return [{
            'currency': 'USD',
            'sum': self.balanceUSD
        }, {
            'currency': 'IQD',
            'sum': self.balanceIQD
        }]'''


'''
@account_router.get('/parent_child_balance')
def parent_child_balance(request, id: int):

    account = Account.objects.get(id=id)
    parent_balance = list(account.balance())

    children = list(account.children.all())
    children_balance = []
    for child in children:
        children_balance = list(child.balance())

    balance_1 = Balance(parent_balance)
    balance_2 = Balance(children_balance)
    parent_children_balances = balance_1 + balance_2
    return parent_children_balances
'''
