from django.contrib import admin
from .models import *
# Register your models here.

class OrderItemAdmin(admin.ModelAdmin):
    list_filter = ('is_canceled',)

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(QrCode)
