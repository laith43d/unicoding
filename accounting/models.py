from pickle import OBJ
from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounting.exceptions import AccountingEquationError
from decimal import Decimal
'''

Account
    - parent
    - type
    - name
    - code
    - full_code
    
Transaction
    - type
    - description

JournalEntry
    - account
    - transaction
    - amount
    - currency
    
* Accounts should support multiple currencies
* Each Transaction should consist of two or more even numbered Journal Entries

'''
class Balance:   
    def __init__(self, balances):

        try:
            balance1 = balances[0]
        except IndexError:
            balance1 = {'currency': 'USD', 'sum': 0}
        try:
            balance2 = balances[1]
        except IndexError:
            if balance1['currency'] == 'USD':
                balance2 = {'currency': 'IQD', 'sum': Decimal(0)}
            else:
                balance2 = {'currency': 'USD', 'sum': Decimal(0)}

        if balance1['currency'] == 'USD':
            balanceUSD = balance1['sum']
            balanceIQD = balance2['sum']
        else:
            balanceIQD = balance1['sum']
            balanceUSD = balance2['sum']

        self.balanceUSD = balanceUSD
        self.balanceIQD = balanceIQD

    def __add__(self, other):
        print(self.balanceIQD)
        self.balanceIQD += other.balanceIQD
        print(self.balanceIQD)
        print(self.balanceUSD)
        self.balanceUSD += other.balanceUSD
        return [{
            'currency': 'USD',
            'sum': self.balanceUSD
        }, {
            'currency': 'IQD',
            'sum': self.balanceIQD
        }]

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
    def __gt__(self, other):

        if self.balanceUSD > other.balanceUSD :
            StaUSD = True
        else:
            StaUSD = False
        if self.balanceIQD > other.balanceIQD :
            StaIQD = True
        else:
            StaIQD = False
        return {'USD':StaUSD},{'IQD':StaIQD}


    def __lt__(self,other):

        if self.balanceUSD < other.balanceUSD :
            StaUSD = True
        else:
            StaUSD = False
        if self.balanceIQD < other.balanceIQD :
            StaIQD = True
        else:
            StaIQD = False
        return {'USD':StaUSD},{'IQD':StaIQD}

    def is_zero(self):
        if self.balanceIQD == 0 and self.balanceUSD == 0 :
            return True
        else:
            return False


class AccountTypeChoices(models.TextChoices):
    ASSETS = 'ASSETS', 'Assets'
    LIABILITIES = 'LIABILITIES', 'Liabilities'
    INCOME = 'INCOME', 'Income'
    EXPENSES = 'EXPENSES', 'Expenses'


class TransactionTypeChoices(models.TextChoices):
    invoice = 'invoice', 'Invoice'
    income = 'income', 'Income'
    expense = 'expense', 'Expense'
    bill = 'bill', 'Bill'


class CurrencyChoices(models.TextChoices):
    USD = 'USD', 'USD'
    IQD = 'IQD', 'IQD'


class Account(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,related_name='children')
    type = models.CharField(max_length=255, choices=AccountTypeChoices.choices)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, null=True, blank=True)
    full_code = models.CharField(max_length=25, null=True, blank=True)
    extra = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f'{self.full_code} - {self.name}'

    def balance(self):
        return self.journal_entries.values('currency').annotate(sum=Sum('amount')).order_by()

    '''this function to amount the blance from 3 ways'''
    def main_balance(self):
        child = self.children.all()
        list_of_balance = []
        if len(child) == 0:
            return self.balance()
        elif len(child) > 0:
            if len(child) == 1:
                return self.balance()
            else:
                for x in child:
                    child_balance = x.balance()
                    OBJ = Balance(child_balance)
                    list_of_balance.append(OBJ)
        return sum(list_of_balance)

class Transaction(models.Model):
    type = models.CharField(max_length=255, choices=TransactionTypeChoices.choices)
    description = models.CharField(max_length=255)

    def validate_accounting_equation(self):
        transaction_sum = self.journal_entries.aggregate(Sum('amount'))['sum']

        if transaction_sum != 0:
            raise AccountingEquationError


class JournalEntry(models.Model):
    class Meta:
        verbose_name_plural = 'Journal Entries'

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='journal_entries')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='journal_entries')
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CurrencyChoices.choices)

    def __str__(self):
        return f'{self.amount} - {self.currency}'
