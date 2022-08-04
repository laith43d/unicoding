from django.contrib import admin

# Register your models here.
from mptt.admin import MPTTModelAdmin

from accounting.models import Account, Transaction, JournalEntry


@admin.register(Account)
class AccountAdmin(MPTTModelAdmin):
    list_display = ['name', 'parent', 'type', 'code', 'full_code']
    search_fields = ['name', 'code', 'full_code']
    list_filter = ['type']
    ordering = ['full_code']


admin.site.register(Transaction)
admin.site.register(JournalEntry)
