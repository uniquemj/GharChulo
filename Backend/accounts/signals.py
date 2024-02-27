from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from .models import *


@receiver(post_save, sender=CustomUser)
def create_customer(sender, instance, created, **kwargs):
    if created and instance.is_customer == True:
        Customer.objects.create(
            user = instance, 
            fullname = f'{instance.first_name} {instance.last_name}'
        )

@receiver(post_save, sender=CustomUser)
def create_kitchen(sender, instance, created, **kwargs):
    if created and instance.is_kitchen == True:
        Kitchen.objects.create(
            user = instance, 
            owned_by = f'{instance.first_name} {instance.last_name}'
        )