from rest_framework.exceptions import ValidationError
from .models import Wallet


"""Функция для проведения операций с кошельком:
1. DEPOSIT - увеличиваем баланс кошелька на указанный amount
2. WITHDRAW - уменьшаем баланс кошелька на указанный amount"""


def perform_operation(wallet: Wallet, operation_type: str, amount: float):
    if operation_type == 'DEPOSIT':
        wallet.balance += amount
    elif operation_type == 'WITHDRAW':
        if wallet.balance < amount:
            raise ValidationError("Insufficient funds")  # Если недостаточно средств, возвращаем ошибку
        wallet.balance -= amount
    else:
        raise ValidationError("Invalid operation type")  # Если неизвестный тип операции - возвращаем ошибку
