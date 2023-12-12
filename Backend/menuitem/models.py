from django.db import models
from django.db.models.query import QuerySet
from accounts.models import *
# Create your models here.

ORDER_STATUS =[
    ('pending','pending'),
    ('in-making','in-making'),
    ('ready','ready')
]
    
class Item(models.Model):
    added_by = models.ForeignKey(Kitchen, related_name='items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=150)
    item_description = models.CharField(max_length=300, null=True, blank=True)
    item_ingredients = models.TextField()
    item_price = models.IntegerField(default=0)
    item_image = models.ImageField(upload_to="item")

    def __str__(self):
        return f'{self.item_name} --> {self.added_by.kitchen_name}'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    kitchen = models.ForeignKey(Kitchen, related_name='orders',on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    address = models.CharField(max_length=100, blank=True)
    phone_no = models.CharField(max_length=10, blank=True)
    is_completed = models.BooleanField(default=False)
    order_status = models.CharField(choices=ORDER_STATUS, max_length=20, default='pending')
    date_ordered = models.DateField(auto_now_add = True)
   
    def __str__(self):
        return f'{self.item.item_name}'
    

class QrCode(models.Model):
    pass