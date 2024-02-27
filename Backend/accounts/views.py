from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .validators import *
from .utils import send_email_token, send_forgot_email
import uuid

# Create your views here.

def CustomerRegistration(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')

        if(password == confirm_password):
            if CustomUser.objects.filter(email = email).exists():
                messages.info(request,'User with this email exists !!')
                return redirect('customer-signup')
            
            #First Name and Last Name should be alphabets
            if not (first_name.isalpha() and last_name.isalpha()):
                messages.error(request, 'First name and last name must contain only alphabets')
                return redirect('customer-signup')
                
            #Email Validation
            try:
                validate_custom_email(email)
            except ValidationError:
                messages.error(request, 'Invalid email format')
                return redirect('customer-signup')

            #Password Validation
            try:
                validate_strong_password(password)
            except ValidationError:
                messages.error(request, 'Password should be more than or equal to 8 digit and make sure to use at least one A-Z, a-z,0-9, and Symbols.')
                return redirect('customer-signup')

            user = CustomUser.objects.create(email = email, first_name = first_name, last_name = last_name, is_customer = True, email_token = str(uuid.uuid4()))
            user.set_password(password)
            user.save()
            send_email_token(user.email, user.email_token)

            return redirect('verificationPage')
        else:
            messages.error(request, "Password and Cofirm Password Doesn't match.")
            return redirect('customer-signup')
    
    return render(request,'accounts/new_customer_signup.html')


def KitchenRegistration(request):
    if request.method == "POST":
        kitchen_name = request.POST.get('kitchen_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        menu = request.FILES.get('menuFile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')

        if(password == confirm_password):

            if CustomUser.objects.filter(email = email).exists():
                messages.info(request,'User with this email exists !!')
                return redirect('kitchen-signup')

            #Kitchen Name should be alphabets
            try:
                validate_name(kitchen_name)
            except ValidationError:
                messages.error(request, 'Kitchen Name must contain only alphabets')
                return redirect('kitchen-signup')

            #First Name and Last Name should be alphabets
            if not (first_name.isalpha() and last_name.isalpha()):
                messages.error(request, 'First name and last name must contain only alphabets')
                return redirect('kitchen-signup')
            
            #Email Validation
            try:
                validate_custom_email(email)
            except ValidationError:
                messages.error(request, 'Invalid email format')
                return redirect('kitchen-signup')
            
            #Phone Number Validation
            try:
                validate_phone_number(phone_number)
            except ValidationError:
                messages.error(request, 'Phone number should be 10 digit number and starts with 98. .')
                return redirect('kitchen-signup')
            
            #Password Validation
            try:
                validate_strong_password(password)
            except ValidationError:
                messages.error(request, 'Password should be more than or equal to 8 digit and make sure to use at least one A-Z, a-z,0-9, and Symbols.')
                return redirect('customer-signup')

            user = CustomUser.objects.create(email = email, first_name = first_name, last_name = last_name,  is_kitchen = True, email_token  = str(uuid.uuid4()))
            user.set_password(password)
            user.save()
            send_email_token(user.email, user.email_token)
            

            kitchen = Kitchen.objects.get(user = user)
            kitchen.kitchen_name = kitchen_name
            kitchen.phone_number = phone_number
            kitchen.menu = menu
            kitchen.save()

            return redirect('verificationPage')
        else:
            messages.error(request, "Password and Cofirm Password Doesn't match.")
            return redirect('kitchen-signup')
    
    return render(request,'accounts/new_kitchen_signup.html')
        

def LoginProcess(request):
    if(request.user.is_authenticated and request.user.is_customer and request.user.is_account_verified):
        return redirect('home')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not CustomUser.objects.filter(email = email).exists():
            messages.info(request,"User with this email doesn't exist !!!")
            return redirect('login-page')
        
        user = authenticate(username = email, password = password)

        if user is None:
            messages.info(request,"Password Incorrect!!!")
            return redirect('login-page')
        else:
            if user.is_customer:
                if user.is_account_verified:
                    login(request,user)
                    return redirect('home')
                else:
                    return redirect('verificationPage')
                
            elif user.is_kitchen and user.is_account_verified:
                kitchen = Kitchen.objects.get(user__email = email)
                if kitchen.is_verified:
                    login(request, user)
                    return redirect('kitchen-dashboard')
                else:
                    return redirect('approvalPending')
    
    
    return render(request,'accounts/new_login_page.html')

def LogoutProcess(request):
    logout(request)
    return redirect('home')

def verificationPage(request):
    return render(request,'accounts/verifyinfo.html')

def verifiedPage(request):
    return render(request,'accounts/verifiedinfo.html')

def verify(request, token):
    try:
        obj = CustomUser.objects.get(email_token = token)
        obj.is_account_verified = True
        obj.save()
        return redirect('verifiedPage')
    
    except Exception as e:
        return HttpResponse("Invalid token")
    
def approvalPending(request):
    return render(request, 'accounts/approvalpending.html')


def ForgotPassword(request):
    if request.user.is_authenticated and request.user.is_customer and request.user.is_account_verified:
        return redirect('home')
    elif request.user.is_authenticated and request.user.is_kitchen and request.user.is_account_verified:
        return redirect('kitchen-dashboard')
    
    if request.method == "POST":
        email = request.POST.get('email')
        if User.objects.filter(email = email).exists():
            user = User.objects.get(email = email)
            user_obj = user.email
            token = str(uuid.uuid4())
            user.email_token = token
            user.save()
            send_forgot_email(user_obj,token)
            messages.success(request,'Email was sent. Please Check your email!!')
            return redirect('login-page')
        else:
            messages.error(request,"User doesn't exit")
            return redirect('forgot-password')
    return render(request,'accounts/forgot-password.html')


def changeForgotPassword(request,token):
    user = User.objects.get(email_token = token)

    if request.method == "POST":
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('password2')

        
        if new_password != confirm_password:
            messages.success(request,'Please provide matching password in both password fields!')
            return redirect(f'change-forgot-password/{token}/')
        
        #Password Validation
        try:
            validate_strong_password(new_password)
        except ValidationError:
            messages.error(request, 'Password should be more than or equal to 8 digit and make sure to use at least one A-Z, a-z,0-9, and Symbols.')
            return redirect('change-forgot-password', token)
        
        user = User.objects.get(email_token = token)
        user.set_password(new_password)
        user.save()
        return redirect('login-page')

    
    return render(request,'accounts/change-forgot-password.html')