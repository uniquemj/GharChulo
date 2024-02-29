from django.db import models
from django.db.models.query import QuerySet
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from accounts.models import *
import json
import uuid
# Create your models here.

ORDER_STATUS =[
    ('pending','pending'),
    ('in-making','in-making'),
    ('ready','ready')
]

PAYMENT_CHOICES = [
    ('Khalti', 'Khalti'),
    ('Cash on Delivery', 'Cash on Delivery')
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
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    order_id =  models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    payment_method = models.CharField(max_length=20, choices = PAYMENT_CHOICES, default = "Cash on Delivery")
    payment_completed = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.order_id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
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
    payment_method = models.CharField(max_length=20, choices = PAYMENT_CHOICES, default = "Cash on Delivery")
    payment_completed = models.BooleanField(default = False)
   
    def __str__(self):
        return f'{self.item.item_name}'
    

class QrCode(models.Model):
    order = models.ForeignKey(Order, related_name = "orderqr", on_delete = models.CASCADE)
    orderItem = models.OneToOneField(OrderItem, related_name= "qrcode", on_delete = models.CASCADE)
    order_code = models.CharField(max_length = 150, editable = False)
    qr_code = models.ImageField(upload_to=f'QRcode', blank=True)

    def __str__(self):
        return f'{self.order.customer.fullname}'

    def save(self, *args, **kwargs):
        data = {
            "order_product_code": self.order_code, 
            "order_phoneNumber": self.orderItem.phone_no, 
            "Payment_Method": self.order.payment_method
        }

        qrcode_image = qrcode.make(json.dumps(data))
        canvas = Image.new('RGB', (680, 645), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        fname = f'qr_code-{self.order_code[:5]}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)