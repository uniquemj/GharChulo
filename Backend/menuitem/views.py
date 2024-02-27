from django.shortcuts import render,redirect
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
import json
import uuid
import requests
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
        payment_method = request.POST.get("payment_method")
        customer = request.user.customer
        

        if payment_method == "Khalti":
            url = "https://a.khalti.com/api/v2/epayment/initiate/"

            return_url = request.POST.get('return_url')
            website_url = request.POST.get('return_url')
            amount = request.POST.get('amount')
            total = int(amount) * 100
            purchase_order_id = request.POST.get('purchase_order_id')

            print("url",url)
            print("return_url",return_url)
            print("web_url",website_url)
            print("amount",amount)
            print("purchase_order_id",purchase_order_id)
            payload = json.dumps({
                "return_url": return_url,
                "website_url": "http://127.0.0.1:8000",
                "amount": str(total),
                "purchase_order_id": purchase_order_id,
                "purchase_order_name": "test",
                "customer_info": {
                "name": customer.fullname,
                "email": customer.user.email,
                "phone": customer.phone_number
                }
            })
            headers = {
                'Authorization': 'key 5ea4ffdb488c40388a4239c6a2f0c7d7',
                'Content-Type': 'application/json',
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)

            new_res = json.loads(response.text)
            print(new_res)
            

            order, created = Order.objects.get_or_create(customer = customer, payment_method = payment_method)
            for item in items:
                kitchen = item.added_by
                orderItem = OrderItem(
                        order = order,
                        customer = customer,
                        kitchen = kitchen,
                        item = item,
                        quantity = cart[str(item.id)],
                        price = item.item_price * cart[str(item.id)],
                        address = address,
                        phone_no = phone_no,
                        payment_method = payment_method,
                        )       
                orderItem.save()  


                order_val = {"order_id": orderItem.id, "order_item": orderItem.item, "order_kitchen": orderItem.kitchen, "order_customer": orderItem.customer, "order_address": orderItem.address, "order_phoneNumber": orderItem.phone_no}
                hash_val = generateSHA256(str(order_val))

                qr_code = QrCode(
                    order = order,
                    orderItem = orderItem,
                    order_code = hash_val
                )
                qr_code.save()
            
            return redirect(new_res['payment_url'])
        
        elif payment_method == "Cash on Delivery":
            print(payment_method)

            order, created = Order.objects.get_or_create(customer = customer, payment_method = payment_method)
            for item in items:
                kitchen = item.added_by
                orderItem = OrderItem(
                        order = order,
                        customer = customer,
                        kitchen = kitchen,
                        item = item,
                        quantity = cart[str(item.id)],
                        price = item.item_price * cart[str(item.id)],
                        address = address,
                        phone_no = phone_no,
                        payment_method = payment_method,
                    ) 
                orderItem.save()  


                order_val = {"order_id": orderItem.id, "order_item": orderItem.item, "order_kitchen": orderItem.kitchen, "order_customer": orderItem.customer, "order_address": orderItem.address, "order_phoneNumber": orderItem.phone_no}
                hash_val = generateSHA256(str(order_val))

                qr_code = QrCode(
                    order = order,
                    orderItem = orderItem,
                    order_code = hash_val
                )
                qr_code.save()

            request.session['cart'] = {}
            return redirect('order-detail')
            

    id = uuid.uuid4()
    context = {  
        'item':items,
        'uuid': id
    }

    return render(request,'menuitem/checkout.html',context)




@login_required(login_url='login-page')
def OrderDetail(request):
    orderItem = OrderItem.objects.filter(customer = request.user.customer).order_by('-date_ordered')

    context = {
        'order':orderItem
    }

    return render(request,'menuitem/customer-order.html',context)


def KitchenOrder(request):
    if not Kitchen.objects.filter(user = request.user).exists():
        logout(request)
        return redirect('login-page')
    
    kitchen = Kitchen.objects.get(user = request.user)
    order = OrderItem.objects.filter(kitchen = kitchen, is_completed = False)
    order_completed = OrderItem.objects.filter(kitchen = kitchen, is_completed = True) 
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

    order = OrderItem.objects.get(id = orderId)
        
    if action == "save":
        order.order_status = order_status
        order.is_completed = is_completed.capitalize()
        order.save()
        
    return JsonResponse('Order Updated!!', safe = False)


def productDetail(request, pk):
    item = Item.objects.get(id = pk)
    kitchen = Kitchen.objects.get(user = item.added_by.user)


    return render(request,'menuitem/product-detail.html',{'item': item,'kitchen': kitchen})

   


def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    pidx = request.GET.get('pidx')
    headers = {
        'Authorization': 'key 5ea4ffdb488c40388a4239c6a2f0c7d7',
        'Content-Type': 'application/json',
    }
    payload = json.dumps({
        'pidx': pidx
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    new_res = json.loads(response.text)
    print(new_res)

    if new_res['status'] == 'Completed':
        customer = request.user.customer
        order = Order.objects.get(customer = customer)
        order.payment_completed = True
        request.session['cart'] = {}
        order.save()

    return redirect('order-detail')
