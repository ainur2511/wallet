from django.urls import path
from .views import WalletDetailView, WalletOperationView, CreateWalletView
from drf_spectacular.views import (SpectacularAPIView,
                                   SpectacularSwaggerView,
                                   SpectacularRedocView)

urlpatterns = [
    path('api/v1/wallets/<uuid:wallet_uuid>/',
         WalletDetailView.as_view(),
         name='wallet-detail'),
    path('api/v1/wallets/<uuid:wallet_uuid>/operation/',
         WalletOperationView.as_view(),
         name='wallet-operation'),
    path('api/v1/wallets/create/',
         CreateWalletView.as_view(),
         name='wallet-create'),
    path('api/schema/',
         SpectacularAPIView.as_view(),
         name='schema'),
    path('api/schema/swagger/',
         SpectacularSwaggerView.as_view(),
         name='swagger'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(),
         name='redoc')
]
