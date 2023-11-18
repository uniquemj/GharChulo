from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from menuitem.models import *
from accounts.models import *
# Create your views here.

@login_required(login_url='login-page')
def home(request):
    page = "home"
    if request.user.is_kitchen:
        kitchen = Kitchen.objects.get(user = request.user)
        queryset = Item.objects.filter(added_by = kitchen)
    else:
        queryset = Kitchen.objects.all()
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    return render(request,'home/home.html',{'page':page,'queryset':queryset,})