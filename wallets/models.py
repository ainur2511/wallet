import uuid
from django.db import models


class Wallet(models.Model):
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False
                            )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.uuid)
