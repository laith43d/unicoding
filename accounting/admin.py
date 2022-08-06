from django.contrib import admin

# Register your models here.
from accounting.models import Account, Transaction, JournalEntry
from mptt.admin import MPTTModelAdmin 

class AccountAdmin(MPTTModelAdmin):
    list_display = ['name', 'parent', 'type', 'code', 'full_code']
    search_fields = ['name', 'code', 'full_code']
    list_filter = ['type']


admin.site.register(Account,AccountAdmin) 
admin.site.register(Transaction)
admin.site.register(JournalEntry)
