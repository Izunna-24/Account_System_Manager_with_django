from django.contrib.auth.models import User
from django.db import models
from .utilities import generate_account_number
from .validators import validate_pin
from django.conf import settings


# Create your models here.


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    ACCOUNT_TYPE = [
        ('S', 'SAVINGS'),
        ('C', 'CURRENT'),
        ('D', 'DOMICILIARY'),
    ]

    account_type = models.CharField(max_length=1, choices=ACCOUNT_TYPE, default='S')
    account_number = models.CharField(max_length=10, default=generate_account_number,
                                      unique=True, primary_key=True)
    pin = models.CharField(max_length=4, validators=[validate_pin], default='0000')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.account_type} {self.balance}"


class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('DEB', 'DEBIT'),
        ('CRE', 'CREDIT'),
        ('TRA', 'TRANSFER'),
    ]
    TRANSACTION_STATUS = [
        ('S', 'SUCCESSFUL'),
        ('F', 'FAILED'),
        ('P', 'PENDING')

    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE, default='CRE')
    transaction_time = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    transaction_status = models.CharField(max_length=1, choices=TRANSACTION_STATUS, default='S')
