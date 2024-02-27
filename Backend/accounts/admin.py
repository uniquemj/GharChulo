from django.contrib import admin
from .models import *
# Register your models here.

class KitchenAdmin(admin.ModelAdmin):
    list_display = ('kitchen_name', 'is_verified')
    list_filter = ('is_verified',)

admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(Kitchen, KitchenAdmin)