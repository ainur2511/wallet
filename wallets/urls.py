from django.urls import path
from .views import WalletDetailView, WalletOperationView

urlpatterns = [
    path('api/v1/wallets/<uuid:wallet_uuid>/', WalletDetailView.as_view(), name='wallet-detail'),
    path('api/v1/wallets/<uuid:wallet_uuid>/operation/', WalletOperationView.as_view(), name='wallet-operation'),
]