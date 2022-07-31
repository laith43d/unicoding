from decimal import Decimal

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

    def total_balance(self):
        children = self.children.all()  # Get all children
        list_balances = []  # Create a list to store balances

        if len(children) == 0:  # If there are no children, return the balance of the account
            return self.balance()

        elif len(children) > 0:  # If there are children, return the balance of the account plus the balance of the
            # children
            if len(children) == 1:  # If there is only one child, return the balance of the child plus the balance of
                # the account
                return self.balance()
            else:  # If there are more than one child, return the balance of the child plus the balance of the child
                # plus the balance of the child
                for child in list(children):  # For each child, add the balance of the child to the list
                    children_balances = child.balance()  # Get the balance of the child
                    obj = Balance(children_balances)  # Create a Balance object from the balance of the child
                    list_balances.append(obj)  # Add the Balance object to the list
        return sum(list_balances)  # Return the sum of all the balances in the list

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
