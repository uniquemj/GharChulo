from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from .manager import UserManager
from .validators import *

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True,validators=[validate_custom_email])
    email_token = models.CharField(max_length = 200)
    is_account_verified = models.BooleanField(default = False)
    is_customer = models.BooleanField(default=False)
    is_kitchen = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    
class KitchenManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_blacklisted = False)

User = get_user_model()

class Customer(models.Model):
    user = models.OneToOneField(User,related_name="customer", on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, validators=[validate_name])
    phone_number = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self)->str:
        return f'{self.fullname}'

class Kitchen(models.Model):
    user = models.OneToOneField(User, related_name="kitchenuser",on_delete=models.CASCADE)
    kitchen_name = models.CharField(max_length=150,null=True, blank=True, validators=[validate_name])
    owned_by = models.CharField(max_length=100, null=True, blank=True, validators=[validate_name])
    image = models.ImageField(upload_to='profile/kitchen',default='profile/kitchen/profile.svg', null=True, blank=True)
    phone_number = models.CharField(max_length=10,null=True, blank=True, validators=[validate_phone_number ])
    menu = models.FileField(upload_to = f"kitchen-menu/")
    service = models.CharField(max_length=250, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=18, null=True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=18, null=True, blank=True)
    is_blacklisted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default = False)
    revenue = models.IntegerField(default=0)

    objects = KitchenManager
    admin_objects = models.Manager

    def __str__(self)->str:
        return f'{self.kitchen_name}'

    class Meta:
        verbose_name = "Kitchen Business"