
from celery.result import AsyncResult
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.db import transaction
from .models import Wallet
from .serializers import WalletSerializer, OperationSerializer
from .tasks import perform_wallet_operation


class WalletDetailView(APIView):
    """Запрос баланса кошелька"""
    serializer_class = WalletSerializer

    def get(self, request, wallet_uuid):
        wallet = get_object_or_404(Wallet, uuid=wallet_uuid)
        serializer = self.serializer_class(wallet)
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
        responses={202: {"description": "Task submitted for processing."}}
    )
    def post(self, request, wallet_uuid):
        wallet = cache.get(wallet_uuid)
        if wallet is None:
            try:
                wallet = Wallet.objects.get(uuid=wallet_uuid)
                # Сохраняем кошелек в кэше на 5 минут
                cache.set(wallet_uuid, wallet, timeout=300)
            except Wallet.DoesNotExist:
                return Response({"error": "Wallet not found."},
                                status=status.HTTP_404_NOT_FOUND)

        serializer = OperationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        operation_type = serializer.validated_data['operationType']
        amount = serializer.validated_data['amount']
        # Вызываем функцию из services.py
        # perform_operation(wallet, operation_type, amount)
        # wallet.save()
        # return Response(WalletSerializer(wallet).data,
        #                 status=status.HTTP_200_OK)
        task = perform_wallet_operation.delay(wallet_uuid,
                                              operation_type,
                                              amount)
        return Response({"task_id": task.id, "status": "processing"},
                        status=status.HTTP_202_ACCEPTED)


class CreateWalletView(generics.CreateAPIView):
    """Создание тестового кошелька"""
    serializer_class = WalletSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskStatusView(APIView):
    def get(self, request, task_id):
        task_result = AsyncResult(task_id)
        if task_result.state == 'PENDING':
            return Response({"status": "PENDING"},
                            status=status.HTTP_200_OK)
        elif task_result.state == 'SUCCESS':
            return Response({"status": "SUCCESS",
                             "result": task_result.result},
                            status=status.HTTP_200_OK)
        elif task_result.state == 'FAILURE':
            return Response({"status": "FAILURE",
                             "error": str(task_result.result)},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": task_result.state},
                            status=status.HTTP_200_OK)
