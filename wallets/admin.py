# from django.contrib import admin
#
# from wallets.models import Wallet
#
#
# @admin.register(Wallet)
# class WalletAdmin(admin.ModelAdmin):
#     list_display = ('uuid', 'balance', 'created_at', 'updated_at')
#     readonly_fields = ('created_at', 'updated_at')
#
#     def get_readonly_fields(self, request, obj=None):
#         if obj:
#             return self.readonly_fields + ('balance',)
#         else:
#             return self.readonly_fields
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#
