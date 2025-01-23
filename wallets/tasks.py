from celery import shared_task
from django.db import transaction
from .models import Wallet
from rest_framework.exceptions import ValidationError


@shared_task(bind=True)
def perform_wallet_operation(self, wallet_uuid,
                             operation_type,
                             amount):
    try:
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(uuid=wallet_uuid)

            if operation_type == 'DEPOSIT':
                wallet.balance += amount
            elif operation_type == 'WITHDRAW':
                if wallet.balance < amount:
                    raise ValidationError("Insufficient funds")
                wallet.balance -= amount
            else:
                raise ValidationError("Invalid operation type")

            wallet.save()
            return {"status": "success", "balance": wallet.balance}
    except Wallet.DoesNotExist:
        return {"status": "error", "message": "Wallet not found"}
    except ValidationError as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        self.retry(exc=e, countdown=5, max_retries=3)
