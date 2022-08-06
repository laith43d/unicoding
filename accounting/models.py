from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounting.exceptions import AccountingEquationError
from mptt.models import MPTTModel, TreeForeignKey

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


class Account(MPTTModel):
    parent = TreeForeignKey('self', 
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

    def save(self, *args, **kwargs):
        # before save
        super(Account, self).save(*args, **kwargs)
        # after save...
        try:
            # get all objects from the Section table.
            trees = Account.objects.all()
            # loops through all values.
            for tree in trees:
                # checks if there is default=0 and if yes rebuild the trees.
                if tree.lft or tree.rght or tree.tree_id == 0:
                    Account.objects.rebuild() 
        except Exception as e:
            pass

    def __str__(self):
        return f'{self.parent_id} - {self.name}'

    def balance(self):
        return self.journal_entries.values('currency').annotate(sum=Sum('amount')).order_by()


    @staticmethod
    def calculate_parent_balance(children_balances):
        sum_USD = 0 
        sum_IQD = 0
        for i in children_balances:
            for j in i:
                if j['currency'] == 'USD' :
                    sum_USD += j['sum']
                else:
                    sum_IQD += j['sum']
        return [sum_USD,sum_IQD]


    def parent_balance(self):
        children_balances = [
            list(account.balance()) for account in self.get_descendants(include_self=True)
        ]

        if len(children_balances[0]): 
            # if the parent has a balance -> calculate the balances of the children and parent 
            sum_USD = Account.calculate_parent_balance(children_balances)[0]
            sum_IQD = Account.calculate_parent_balance(children_balances)[1]
        else: 
            # else -> calculate the balances of the children only which starts from the 2nd list
            sum_USD = Account.calculate_parent_balance(children_balances[1:])[0]
            sum_IQD = Account.calculate_parent_balance(children_balances[1:])[1]

        return [{
            'currency': 'USD',
            'sum':sum_USD
        }, 
        {
            'currency': 'IQD',
            'sum': sum_IQD
        }]  



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
