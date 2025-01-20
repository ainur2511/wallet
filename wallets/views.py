from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import status
from django.db import transaction

from .models import Wallet
from .serializers import WalletSerializer, OperationSerializer
from .services import perform_operation

"""Запрос баланса кошелька"""


class WalletDetailView(APIView):
    # def get(self, request, wallet_uuid):
    #     wallet = get_object_or_404(Wallet, uuid=wallet_uuid)
    #     # balance = Wallet.objects.filter(uuid=wallet_uuid).values_list('balance', flat=True)
    #     serializer = WalletSerializer(wallet)
    #     # if balance is None:
    #     #     return Response({"detail": "Wallet not found"}, status=404)
    #     return Response(serializer.data)
    #     # return Response({"balance": str(balance)}, status=200)

    def get(self, request, wallet_uuid):
        # Извлекаем только нужные поля из базы данных
        balance = Wallet.objects.filter(uuid=wallet_uuid).values('balance').first()

        # Если объект не найден, возвращаем 404
        if not balance:
            return Response({"detail": "Not found."}, status=404)

        return Response(balance)


"""Проведение операций с кошельком:
"""


class WalletOperationView(APIView):
    @transaction.atomic
    def post(self, request, wallet_uuid):
        try:
            wallet = Wallet.objects.select_for_update().get(uuid=wallet_uuid)
        except Wallet.DoesNotExist:
            raise NotFound("Wallet not found")

        serializer = OperationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        operation_type = serializer.validated_data['operationType']
        amount = serializer.validated_data['amount']

        perform_operation(wallet, operation_type, amount)  # Вызываем функцию из services.py

        wallet.save()
        return Response(WalletSerializer(wallet).data, status=status.HTTP_200_OK)
