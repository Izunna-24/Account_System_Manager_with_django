from rest_framework import serializers
from .models import Account, Transaction
from account.models import Account


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_time', 'transaction_type', 'description']


class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)

    # transactions = serializers.StringRelatedField()
    class Meta:
        model = Account
        fields = ['account_number', 'balance', 'account_type', 'transactions']


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user', 'account_number', 'pin', 'account_type']


class DepositWithdrawSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)


class TransferSerializer(serializers.Serializer):
    sender_account = serializers.CharField(max_length=10)
    receiver_account = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
