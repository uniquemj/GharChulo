from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *

# Create your views here.

def CustomerRegistration(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if CustomUser.objects.filter(email = email).exists():
            messages.info(request,'User with this email exists !!')
            return redirect('customer-signup')
        
        user = CustomUser.objects.create(email = email, first_name = first_name, last_name = last_name, is_customer = True)
        user.set_password(password)
        user.save()
        messages.success(request,'Customer Registration Completed!!')
        return redirect('customer-signup')
    
    return render(request,'accounts/customer_signup.html')


def KitchenRegistration(request):
    if request.method == "POST":
        kitchen_name = request.POST.get('kitchen_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if CustomUser.objects.filter(email = email).exists():
            messages.info(request,'User with this email exists !!')
            return redirect('kitchen-signup')
        
        user = CustomUser.objects.create(email = email, first_name = first_name, last_name = last_name,  is_kitchen = True)
        user.set_password(password)
        user.save()

        kitchen = Kitchen.objects.get(user = user)
        kitchen.kitchen_name = kitchen_name
        kitchen.save()
        messages.success(request,'Kitchen Registration Completed!!')
        return redirect('kitchen-signup')
    
    return render(request,'accounts/kitchen_signup.html')
        

def LoginProcess(request):
    if(request.user.is_authenticated and request.user.is_customer):
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
            login(request,user)
            return redirect('home')
    
    return render(request,'accounts/login_page.html')

def LogoutProcess(request):
    logout(request)
    return redirect('login-page')