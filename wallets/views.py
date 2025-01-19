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
    def get(self, request, wallet_uuid):
        wallet = get_object_or_404(Wallet, uuid=wallet_uuid)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)


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
