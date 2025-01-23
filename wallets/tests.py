import uuid

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Wallet
from decimal import Decimal


class WalletAPITests(APITestCase):
    def setUp(self):
        # Создаем тестовый кошелек
        self.wallet = Wallet.objects.create(balance=100.00)
        self.wallet_uuid = self.wallet.uuid

    def test_get_wallet_detail(self):
        url = reverse('wallet-detail', args=[self.wallet_uuid, ])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'uuid': str(self.wallet.uuid),
            'balance': f'{self.wallet.balance:.2f}'
        })

    def test_get_wallet_detail_not_found(self):
        non_existent_uuid = uuid.uuid4()
        url = reverse('wallet-detail', args=[non_existent_uuid])
        response = self.client.get(url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {
            "detail": "No Wallet matches the given query.",
        })

    def test_post_wallet_operation_deposit(self):
        url = reverse('wallet-operation', args=[self.wallet_uuid])
        data = {
            'operationType': 'DEPOSIT',
            'amount': '50.00'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal('150.00'))

    def test_post_wallet_operation_withdraw(self):
        url = reverse('wallet-operation', args=[self.wallet_uuid])
        data = {
            'operationType': 'WITHDRAW',
            'amount': '30.00'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal('70.00'))

    def test_post_wallet_operation_withdraw_insufficient_funds(self):
        url = reverse('wallet-operation', args=[self.wallet_uuid])
        data = {
            'operationType': 'WITHDRAW',
            'amount': '200.00'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Insufficient funds", str(response.data))

    def test_post_wallet_operation_invalid_type(self):
        url = reverse('wallet-operation', args=[self.wallet_uuid])
        data = {
            'operationType': 'INVALID_TYPE',
            'amount': '50.00'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
