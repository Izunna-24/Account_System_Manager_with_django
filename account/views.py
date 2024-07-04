from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Account, Transaction
from .serializers import AccountSerializer, AccountCreateSerializer, DepositWithdrawSerializer


# Create your views here.


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer


# class ListAccount(ListCreateAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountCreateSerializer

# def get_queryset(self):
#     return Account.objects.all()
#
# def get_serializer_class(self):
#     return AccountCreateSerializer

# def get(self, request):
#     accounts = Account.objects.all()
#     serializer = AccountCreateSerializer(accounts, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
# def post(self, request):
#     serializer = AccountCreateSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['GET', 'POST'])
# def list_account(request):
#     if request.method == 'GET':
#         accounts = Account.objects.all()
#         serializer = AccountSerializer(accounts, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = AccountCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class AccountDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountCreateSerializer

# def get(self, request, pk):
#     account = get_object_or_404(Account, pk=pk)
#     serializer = AccountSerializer(account)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
# def put(self, request, pk):
#     account = get_object_or_404(Account, pk=pk)
#     serializer = AccountCreateSerializer(account, data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
# def delete(self, request, pk):
#     account = get_object_or_404(Account, pk=pk)
#     account.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(["GET", "PUT", "PATCH", "DELETE"])
# def account_detail(request, pk):
#     account = get_object_or_404(Account, pk=pk)
#     if request.method == 'GET':
#         serializer = AccountSerializer(account)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'PUT':
#         serializer = AccountCreateSerializer(account, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'DELETE':
#         account.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class Deposit(APIView):
    def post(self, request):
        serializer = DepositWithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = request.data['account_number']
        amount = Decimal(request.data['amount'])
        transaction_details = {}
        account = get_object_or_404(Account, pk=account_number)
        balance = account.balance
        balance += amount
        Account.objects.filter(account_number=account_number).update(balance=balance)
        Transaction.objects.create(
            account=account,
            amount=amount
        )
        transaction_details['account_number'] = account_number
        transaction_details['amount'] = amount
        transaction_details['transaction_type'] = 'CREDIT'

        return Response(data=transaction_details,
                        status=status.HTTP_200_OK)


class Withdrawal(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        account_number = request.data['account_number']
        amount = request.data['amount']
        pin = request.data['pin']
        account = get_object_or_404(Account, pk=account_number)
        if account.pin == pin:
            if account.balance > amount:
                account.balance -= Decimal(amount)
                account.save()
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='DEBIT'
                )
            else:
                return Response(data={'message': 'Insufficient balance'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'message': 'pin is invalid'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'message': 'Transaction successful'}, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def deposit(request):
#     account_number = request.data['account_number']
#     amount = Decimal(request.data['amount'])
#     account = get_object_or_404(Account, pk=account_number)
#     account.balance += amount
#     account.save()
#     Transaction.objects.create(
#         account=account,
#         amount=amount
#     )
#     return Response(data={'message': 'Transaction successful'}, status=status.HTTP_200_OK)


# def withdraw(request):
# account_number = request.data['account_number']
# amount = request.data['amount']
# pin = request.data['pin']
# account = get_object_or_404(Account, pk=account_number)
# if account.pin == pin:
#     if account.balance > amount:
#         account.balance -= Decimal(amount)
#         account.save()
#         Transaction.objects.create(
#             account=account,
#             amount=amount,
#             transaction_type='DEB'
#         )
#     else:
#         return Response(data={'message': 'Insufficient balance'},
#                         status=status.HTTP_400_BAD_REQUEST)
# else:
#     return Response(data={'message': 'pin is invalid'},
#                     status=status.HTTP_400_BAD_REQUEST)
# return Response(data={'message': 'Transaction successful'}, status=status.HTTP_200_OK)

# class CreateAccount(CreateAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountCreateSerializer
