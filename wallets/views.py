from django.shortcuts import render, get_object_or_404
from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import status, generics
from django.db import transaction

from .models import Wallet
from .serializers import WalletSerializer, OperationSerializer
from .services import perform_operation


class WalletDetailView(APIView):
    """Запрос баланса кошелька"""
    def get(self, request, wallet_uuid):
        wallet = get_object_or_404(Wallet, uuid=wallet_uuid)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)




class WalletOperationView(APIView):
    """Проведение операций с кошельком.
    для параметра operationType:
    DEPOSIT - увеличиваем баланс кошелька на указанный amount
    WITHDRAW - уменьшаем баланс кошелька на указанный amount
    """
    @transaction.atomic
    @extend_schema(
        request=OperationSerializer,
        responses={200: WalletSerializer}
    )
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


class CreateWalletView(generics.CreateAPIView):
    """Создание тестового кошелька"""
    serializer_class = WalletSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
