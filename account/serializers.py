from rest_framework import serializers
from .models import Account, Transaction
from account.models import Account


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_time', 'transaction_type', 'description']


class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)

    class Meta:
        model = Account
        fields = ['account_number', 'first_name', 'last_name', 'balance', 'account_type',
                  'transactions']

    # transactions = serializers.StringRelatedField()


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'pin', 'account_type']
