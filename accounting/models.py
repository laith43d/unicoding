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
        if other == 0:  #
            return self
        else:
            return self.__add__(other)

    def __gt__(self, other):
        obj_balance1 = self.balanceUSD > other.balanceIQD
        obj_balance2 = self.balanceIQD > other.balanceUSD
        return obj_balance1, obj_balance2

    def __lt__(self, other):
        obj_balance1 = self.balanceUSD < other.balanceUSD
        obj_balance2 = self.balanceIQD < other.balanceIQD
        return obj_balance1, obj_balance2

    def e_t_z(self):
        if self.balanceUSD == 0 and self.balanceIQD == 0:
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

        def main_balance(self):
            child = self.children.all()
            list_of_balances = []

            if len(child) == 0:
                return self.balance()

            elif len(child) > 0:
                if len(child) == 1:
                    return self.balance()
                else:
                    for k in list(child):
                        list_of_child = k.balance()
                        obj = Balance(list_of_child)
                        list_of_balances.append(obj)
            return sum(list_of_balances)

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
