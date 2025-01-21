from rest_framework import serializers
from .models import Wallet


def validate_score(score):
    if score <= 0:
        raise serializers.ValidationError("Amount must be greater than zero")
    return score


class WalletSerializer(serializers.ModelSerializer):
    """Сериализатор для кошелька"""
    class Meta:
        model = Wallet
        fields = ['uuid', 'balance', ]

    def validate_balance(self, value):
        return validate_score(value)


class OperationSerializer(serializers.Serializer):
    """Сериализатор для POST запроса на изменение баланса """
    operationType = serializers.ChoiceField(choices=['DEPOSIT', 'WITHDRAW'])
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    # Валидируем, чтобы число amount было положительным
    def validate_amount(self, value):
        return validate_score(value)
