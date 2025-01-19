from rest_framework import serializers
from .models import Wallet

"""Сериализатор для GET-запроса"""


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['uuid', 'balance', ]


"""Сериализатор для POST запроса на изменение баланса """


class OperationSerializer(serializers.Serializer):
    operationType = serializers.ChoiceField(choices=['DEPOSIT', 'WITHDRAW'])
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    # Валидируем, чтобы число amount было положительным
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value
