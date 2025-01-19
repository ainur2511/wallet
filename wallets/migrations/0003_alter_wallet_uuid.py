# Generated by Django 5.1.5 on 2025-01-18 11:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0002_wallet_created_at_wallet_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
