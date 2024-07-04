from django.contrib import admin
from .models import Account


# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'account_type', 'balance']
    list_per_page = 10
    list_editable = [ 'account_type', 'balance']
