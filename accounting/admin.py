from django.contrib import admin

# Register your models here.
from accounting.models import Account, Transaction, JournalEntry


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'type', 'code', 'full_code']
    search_fields = ['name', 'code', 'full_code']
    list_filter = ['type']
    ordering = ['full_code']

@admin.register(JournalEntry)
class JEAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'currency']



admin.site.register(Transaction)

