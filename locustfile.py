from locust import HttpUser, task, between
import random
# import uuid


class WalletUser(HttpUser):
    wait_time = between(1, 2)  # Время ожидания между запросами
    wallet_uuid = '1ff65aea-9739-48aa-85e0-c851ae0a9d93'
    @task
    def get_wallet_detail(self):
        # Выполняем GET-запрос к эндпоинту для получения деталей кошелька
        response = self.client.get(f"/api/v1/wallets/{self.wallet_uuid}/")
        if response.status_code == 404:
            print(f"Wallet not found: {self.wallet_uuid}")
        else:
            print(f"Wallet details retrieved: {response.content}")

    # @task
    # def post_wallet_operation(self):
    #     wallet_uuid = self.wallet_uuid
    #     # Подготавливаем данные для POST-запроса
    #     operation_type = random.choice(['DEPOSIT', 'WITHDRAW'])
    #     amount = round(random.uniform(1, 100), 2)  # Случайная сумма от 1 до 100
    #     data = {
    #         'operationType': operation_type,
    #         'amount': str(amount)
    #     }
    #     # Выполняем POST-запрос к эндпоинту для выполнения операции с кошельком
    #     response = self.client.post(f"/api/v1/wallets/{wallet_uuid}/operation/", json=data)
    #     if response.status_code == 200:
    #         print(f"Operation successful: {response.json()}")
    #     else:
    #         print(f"Operation failed: {response.status_code}, {response.text}")