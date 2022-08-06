from django.contrib import admin

from accounting.models import Account, Transaction, JournalEntry


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent', 'type', 'code', 'full_code']
    search_fields = ['name', 'code', 'full_code']
    list_filter = ['type']
    ordering = ['full_code']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'description']


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'currency', 'account_id', 'transaction_id']
