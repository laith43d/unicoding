from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounting.exceptions import AccountingEquationError


class Balance():

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


    def __sub__(self, other):
        self.balanceIQD -= other.balanceIQD
        self.balanceUSD -= other.balanceUSD
        return [{
            'currency': 'USD',
            'sum': self.balanceUSD
        }, {
            'currency': 'IQD',
            'sum': self.balanceIQD
        }]

    def __gt__(self, other):
        return self.balanceUSD > other.balanceUSD, self.balanceIQD > other.balanceIQD

    def __lt__(self, other):
        return self.balanceUSD < other.balanceUSD, self.balanceIQD < other.balanceIQD

    def is_zero(self):
        return self.balanceUSD == 0 and self.balanceIQD == 0


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
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=255, choices=AccountTypeChoices.choices)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, null=True, blank=True)
    full_code = models.CharField(max_length=25, null=True, blank=True)
    extra = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f'{self.full_code} - {self.name}'

    def balance(self):
        return self.journal_entries.values('currency').annotate(sum=Sum('amount')).order_by()
    
    def Balance_Sum(self):
        children = self.account_children.all()  
        balances = [] 

        if len(children) == 0: 
            return self.balance()

        elif len(children) > 0: 
            
            if len(children) == 1:  
                
                return self.balance()
            else:  

                for childrens in list(children): 
                    children_balances = childrens.balance()  
                    chilrenOBJ = Balance(children_balances) 
                    balances.append(chilrenOBJ) 
        return sum(balances)
    

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
