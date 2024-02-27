from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
import re

def validate_custom_email(value):
    # First, validate the email using Django's built-in validator
    try:
        validate_email(value)
    except ValidationError:
        raise ValidationError('Invalid email format')

    # Then check if the email matches the restricted pattern
    if value.lower() == 'abc@gmail.com':
        raise ValidationError('Email not allowed')



def validate_name(value):
    # Define a regular expression pattern to allow only alphabets and spaces
    pattern = r'^[a-zA-Z ]+$'

    # Check if the value matches the pattern
    if not re.match(pattern, value):
        raise ValidationError(
            _('Only alphabets and spaces are allowed in the name.'),
            code='invalid_name'
        )



def validate_phone_number(value):
    # Check if the phone number is exactly 10 digits long
    if len(value) != 10:
        raise ValidationError('Phone number must be exactly 10 digits long')
    

def validate_strong_password(value):
    # Check if the password contains at least 8 characters
    if len(value) < 8:
        raise ValidationError('Password must contain at least 8 characters')

    # Check if the password contains at least one uppercase letter
    if not re.search('[A-Z]', value):
        raise ValidationError('Password must contain at least one uppercase letter')

    # Check if the password contains at least one lowercase letter
    if not re.search('[a-z]', value):
        raise ValidationError('Password must contain at least one lowercase letter')

    # Check if the password contains at least one digit
    if not re.search('[0-9]', value):
        raise ValidationError('Password must contain at least one digit')

    # Check if the password contains at least one special character
    if not re.search('[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError('Password must contain at least one special character')
    

def validate_phone_number(value):
    # Check if the phone number is exactly 10 digits long
    if len(value) != 10:
        raise ValidationError('Phone number must be exactly 10 digits long')
    
    # Check if the phone number starts with '98'
    if not value.startswith('98'):
        raise ValidationError('Phone number must start with 98')

    # Check if the phone number contains only digits
    if not value.isdigit():
        raise ValidationError('Phone number must contain only digits')