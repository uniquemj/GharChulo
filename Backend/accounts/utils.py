from django.conf import settings
from django.core.mail import send_mail

def send_email_token(email, token):
    
    subject = "Verify Your Registration to GharChulo"
        
    message = f""" Dear User,

Thank you for registering with GharChulo! To ensure the security of your account and to complete the registration process, we kindly ask you to verify your email address.

Please follow the simple steps below to verify your account:
 
    1. Click on the following link: http://127.0.0.1:8000/verify/{token}/
    2. Once the page loads, you will be automatically verified, and your registration process will be complete.

If you did not register for GharChulo, please ignore this email.

Thank you for choosing GharChulo. If you encounter any issues or need further assistance, please don't hesitate to contact our support team at ghar.chulo2023@gmail.com.

Best regards,

Team GharChulo
"""
    email_from =  settings.EMAIL_HOST_USER
    recipient_list = [email]
    print(email)

    send_mail(subject, message, email_from, recipient_list)
    
    
    
def send_forgot_email(email, token):
    subject = "Your forgot password link"
    message = f'Hi There click in given link to reset your password : http://127.0.0.1:8000/change-forgot-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    receipt = [email]

    send_mail(subject,message,email_from,receipt,fail_silently = False)
    return True

    