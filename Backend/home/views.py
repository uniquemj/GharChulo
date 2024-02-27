from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from menuitem.models import *
from accounts.models import *
from .utils import getNearestKitchen
# Create your views here.


def home(request):
    page = "home"
    if not request.user.is_authenticated:
        return render(request,'home/home.html')
    
    if not request.user.is_customer:
        return redirect('login-page')
    lat = request.POST.get('currentLatitude')
    lng = request.POST.get('currentLongitude')

    location = request.session.get('location')
    kitchen = []
    if location:
        latitude = location['lat']
        longitude = location['lng']
        kitchen = getNearestKitchen(latitude, longitude)
    

    request.session['location'] = {'lat': lat, 'lng': lng}

    query =  request.GET.get('food-search') if request.GET.get('food-search')!=None else ''

    items = []
    if(len(query)>0):
        page = "search"
        if kitchen:
            items = Item.objects.filter(
                Q(item_name__contains = query) &
                Q(added_by__kitchen_name__in = kitchen)
                )
    
    queryset = []
    if kitchen:
        queryset = Kitchen.objects.filter(kitchen_name__in = kitchen)
    
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    return render(request,'home/new_home.html',{'page':page,'queryset':queryset,'items':items, 'query':query})

def kitchendashboard(request):
    if not request.user.is_authenticated:
        return render(request,'home/home.html')
    if not request.user.is_kitchen:
        return redirect('login-page')
    kitchen = Kitchen.objects.get(user = request.user)
    context = {
        'user':kitchen
    }
    return render(request,'home/kitchen-dashboard-profile.html', context) 

def kitchenDashboardProduct(request):
    if not request.user.is_authenticated:
        return render(request,'home/home.html')
    if not request.user.is_kitchen:
        return redirect('login-page')
    kitchen = Kitchen.objects.get(user = request.user)
    queryset = Item.objects.filter(added_by = kitchen)
    return render(request,'home/kitchen-dashboard-product.html',{'queryset':queryset,})

def kitchenPage(request, name):
    if not request.user.is_authenticated:
        return render(request,'home/home.html')
    page = "kitchenPage"
    kitchen = Kitchen.objects.get(kitchen_name = name)
    context = {
        'kitchen':kitchen,
        'page' : page
    }
    return render(request,'home/kitchen-page.html', context)

def kitchenSetting(request):
    if not request.user.is_authenticated:
        return render(request,'home/home.html')
    if not request.user.is_kitchen:
        return redirect('login-page')
    user = request.user
    kitchen = Kitchen.objects.get(user = user)
    if not kitchen.location and kitchen.latitude!=0 and kitchen.longitude!=0:
        status = False
    else:
        status = True

    if request.method == "POST":
        kitchen_name = request.POST.get('kitchen_name')
        owned_by = request.POST.get('owned_by')
        image = request.FILES.get('image')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        service = request.POST.get('service')
        
        if not status:
            location = request.POST.get('location')
            latitude = request.POST.get('lat')
            longitude = request.POST.get('lng')
            kitchen_location = request.session.get('kitchen_location')
            if location != None and latitude != None and longitude!= None:
                print(location)
                request.session['kitchen_location'] = {'location': location, 'lat': latitude, 'lng': longitude}
            
        if image:
            kitchen.image = image
            
        kitchen_location = request.session.get('kitchen_location')
        
        if kitchen_location:
            kitchen.user.email = email
            kitchen.kitchen_name = kitchen_name
            kitchen.owned_by = owned_by
            kitchen.phone_number = phone_number
            kitchen.service = service
            kitchen.location = kitchen_location['location']
            kitchen.latitude = kitchen_location['lat']
            kitchen.longitude = kitchen_location['lng']
        else:
            return redirect('setting')
    
        kitchen.save()

        return redirect('setting')

    context = {
        'kitchen':kitchen,
        'status':status
    }

    return render(request, 'home/kitchen-dashboard-setting.html',context)