from typing import List, Any

from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounting.exceptions import AccountingEquationError

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


class Balance:
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
            'currency': 'IQD',
            'sum': self.balanceIQD
        }, {
            'currency': 'USD',
            'sum': self.balanceUSD
        }]

    def __gt__(self, other):
        bIQD = self.balanceIQD > other.balanceIQD
        bUSD = self.balanceUSD > other.balanceUSD
        return bIQD, bUSD

    def __lt__(self, other):
        bIQD = self.balanceIQD < other.balanceIQD
        bUSD = self.balanceUSD < other.balanceUSD
        return bIQD, bUSD

    def is_zero(self):
        bIQD = True if self.balanceIQD == 0 else False
        bUSD = True if self.balanceUSD == 0 else False
        return bIQD, bUSD


class Account(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    type = models.CharField(max_length=255, choices=AccountTypeChoices.choices)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, null=True, blank=True)
    full_code = models.CharField(max_length=25, null=True, blank=True)
    extra = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f'{self.full_code} - {self.name}'

    def balance(self):
        return self.journal_entries.values('currency').annotate(sum=Sum('amount')).order_by()

    @property
    def parent_balances(self):
        global total_balance
        parent_children = self.children.all()
        for account in parent_children:
            balance_acc = Balance(account.balance())
            children = self.children.all()
            for child_obj in children:
                balance_acc_obj = Balance(child_obj.balance())
                total_balance = balance_acc_obj.__add__(balance_acc)
            return total_balance


# def save(
#         self, force_insert=False, force_update=False, using=None, update_fields=None
# ):
#     creating = not bool(self.id)
#
#     if creating:
#         self.code = self.id
#         try:
#             self.full_code = f'{self.parent.full_code}{self.id}'
#         except AttributeError:
#             self.full_code = self.id
#
#     super(Account, self).save()
#
#     if creating:
#         self.refresh_from_db()


# @receiver(post_save, sender=Account)
# def add_code_and_full_code(sender, instance, **kwargs):
#     instance.code = instance.id
#     if instance.parent:
#         instance.full_code = f'{instance.parent.full_code}{instance.id}'
#     else:
#         instance.full_code = f'{instance.id}'


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
