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


# class Balance:
#     def __init__(self, balances):
#         balanceIQD = 0
#         balanceUSD = 0
#         for i in balances:
#             if i['currency'] == 'USD':
#                 balanceUSD = i['sum']
#             if i['currency'] == 'IQD':
#                 balanceIQD = i['sum']


#         self.balanceUSD = balanceUSD
#         self.balanceIQD = balanceIQD

#     def __add__(self, other):
#         self.balanceIQD += other.balanceIQD
#         self.balanceUSD += other.balanceUSD
#         return [{
#             'currency': 'USD',
#             'sum': self.balanceUSD
#         }, {
#             'currency': 'IQD',
#             'sum': self.balanceIQD
#         }]


class Account(models.Model):
    parent = models.ForeignKey('self', 
                               null=True, 
                               blank=True, 
                               on_delete=models.SET_NULL,
                               related_name='children'
                              )
    type = models.CharField(max_length=255, choices=AccountTypeChoices.choices)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, null=True, blank=True)
    full_code = models.CharField(max_length=25, null=True, blank=True)
    extra = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f'{self.parent_id} - {self.name}'

    def balance(self):
        return self.journal_entries.values('currency').annotate(sum=Sum('amount')).order_by()


    def parent_balance(self):
        children = self.children.all()
        
        if len(children) == 0:   
            return self.balance()

        if len(children) == 1:  
            return list(children[0].balance())
        
        children_balances = [ list(c.balance()) for c in children ]
        
        sum_USD = 0
        sum_IQD = 0 

        for lst in children_balances:   
            for child in lst: 
                if child['currency'] == 'USD':
                    sum_USD += child['sum']
                else:
                    sum_IQD += child['sum']

        return [{
            'currency': 'USD',
            'sum':sum_USD
        }, 
        {
            'currency': 'IQD',
            'sum': sum_IQD
        }]  


        # balances_objects = [ Balance(i) for i in children_balance ]
        # p = 0
        # for i in range(len(balances_objects)) :
        #     p = balances_objects[i].__add__(balances_objects[i+1])
        #     if i+1 == len(balances_objects)-1:
        #         break
        # return p


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
