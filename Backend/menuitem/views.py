from django.shortcuts import render,redirect
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
import json
from .utils import generateSHA256
from .models import *
from accounts.models import *
# Create your views here.

# This function is use for adding product by Kitchen Owner
@login_required(login_url='login-page')
def AddProduct(request):
    if request.method =="POST":
        item_name = request.POST.get('item_name')
        item_description = request.POST.get('item_description')
        item_price = request.POST.get('item_price')
        item_ingredients = request.POST.get('item_ingredients')
        item_image = request.FILES.get('item_image')
        
        added_by = Kitchen.objects.get(user = request.user)

        if item_name != None and item_price != None and item_image != None:
            Item.objects.create(
                added_by = added_by,
                item_name = item_name,
                item_description = item_description,
                item_ingredients = item_ingredients,
                item_price = item_price,
                item_image = item_image
            )
            messages.success(request,'Product Added !!')
            return redirect('kitchen-product')
        
        else:
            return redirect('kitchen-product')
        
    
    return render(request,'menuitem/product.html')


#This function is use for editing the details of existing product by only product owner.
@login_required(login_url='login-page')
def editProduct(request, id):
    item = Item.objects.get(id = id)
    if request.method == "POST":
        item_name = request.POST.get('item_name')
        item_description = request.POST.get('item_description')
        item_price = request.POST.get('item_price')
        item_ingredients = request.POST.get('item_ingredients')
        item_image = request.FILES.get('item_image')

        if item_image:
            item.item_image = item_image
        
        item.item_name = item_name
        item.item_description = item_description
        item.item_price = item_price
        item.item_ingredients = item_ingredients

        item.save()
        messages.success(request,'Product Updated!!!')
        return redirect('kitchen-product')
    
    return render(request,'menuitem/edit-product.html',{'item': item})


# This product is use for deleting the product by only owner
@login_required(login_url='login-page')
def deleteProduct(request,id):
    item = Item.objects.get(id = id)
    if request.user != item.added_by:
        return redirect('kitchen-product')
    
    item.delete()
    return redirect('kitchen-product')


# This function is use for accessing the cart page.
@login_required(login_url='login-page')
def new_cart(request):
    ids = list(request.session.get('cart').keys())
    item = Item.objects.filter(id__in = ids)

    context = {
        'queryset': item
    }

    return render(request,'menuitem/cart.html', context)



#adds to card or update items in cart
@login_required(login_url='login-page')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    cart = request.session.get('cart')
    if cart:
        quantity = cart.get(productId)

        if action == "add":
            messages.info(request,"Item Added to Cart!")
            if quantity:
                cart[productId] = quantity + 1
            else:
                cart[productId] = 1 
        elif action =="remove":
            messages.info(request,"Item Removed to Cart!")
            if quantity<=1:
                cart.pop(productId)
            else:
                cart[productId] = quantity - 1
            
        elif action == "delete":
            cart.pop(productId)
    else:
        cart = {}
        cart[productId] = 1
    
    request.session['cart'] = cart
    
    return JsonResponse('Item Added!!', safe=False)

@login_required(login_url='login-page')
def checkout(request):
    cart = request.session.get('cart')
    items = Item.objects.filter(id__in = list(cart.keys()))
    
    if request.method == "POST":
        address = request.POST.get('address')
        phone_no = request.POST.get('phone_no')
        payment_method = request.POST.get('payment_method')
        total_amount = request.POST.get("total_amount")
        print(total_amount)

        customer = request.user.customer
        if payment_method == "Cash on Delivery":
            payment_completed = False
        elif payment_method =="Khalti":
            payment_completed = True

        for item in items:
            kitchen = item.added_by
            order = Order(
                    customer = customer,
                    kitchen = kitchen,
                    item = item,
                    quantity = cart[str(item.id)],
                    price = item.item_price * cart[str(item.id)],
                    address = address,
                    payment_method = payment_method,
                    phone_no = phone_no,
                    payment_completed = payment_completed
                ) 
            order.save()  

            if order.payment_completed:
                kitchen.revenue += order.price
                kitchen.save()

            order_val = {"order_id": order.id, "order_item": order.item, "order_kitchen": order.kitchen, "order_customer": order.customer, "order_address": order.address, "order_phoneNumber": order.phone_no}
            hash_val = generateSHA256(str(order_val))

            qr_code = QrCode(
                order = order,
                order_code = hash_val
            )
            qr_code.save()
            request.session['cart'] = {}
        messages.info(request, "Order have been placed!!")
        if payment_method == "Khalti":
            return redirect(reverse("khalti-request")+"?order_total="+total_amount)
        return redirect('order-detail')
    
    context = {  
        'item':items
    }

    return render(request,'menuitem/checkout.html',context)


class KhaltiRequestView(View):
    def get(self,request, *args, **kwargs):
        total_amount = request.GET.get('order_total')
        context = {
            'total_amount': total_amount
        }
        return render(request,'menuitem/khaltirequest.html', context)

class KhaltiVerifyView(View):
    def get(self, request, *args, **kwargs):
        data = {}
        return JsonResponse(data)

@login_required(login_url='login-page')
def OrderDetail(request):
    order = Order.objects.filter(customer = request.user.customer).order_by('-date_ordered')

    context = {
        'order':order
    }

    return render(request,'menuitem/customer-order.html',context)


def KitchenOrder(request):
    if not Kitchen.objects.filter(user = request.user).exists():
        logout(request)
        return redirect('login-page')
    
    kitchen = Kitchen.objects.get(user = request.user)
    order = Order.objects.filter(kitchen = kitchen, is_completed = False)
    order_completed = Order.objects.filter(kitchen = kitchen, is_completed = True) 
    context = {
        'order':order,
        'order_completed':order_completed,

    }

    return render(request,'menuitem/kitchenorder.html',context)

def updateOrder(request):
    orderId = request.POST.get('orderId')
    action = request.POST.get('action')
    order_status = request.POST.get('order_status')
    is_completed = request.POST.get('is_completed')

    order = Order.objects.get(id = orderId)
        
    if action == "save":
        order.order_status = order_status
        order.is_completed = is_completed.capitalize()
        order.save()
        
    return JsonResponse('Order Updated!!', safe = False)


def productDetail(request, pk):
    item = Item.objects.get(id = pk)
    kitchen = Kitchen.objects.get(user = item.added_by.user)


    return render(request,'menuitem/product-detail.html',{'item': item,'kitchen': kitchen})