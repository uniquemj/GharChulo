from django.urls import path
from accounts.views import *
from menuitem.views import *
from .views import *

urlpatterns = [
    path('',home,name = "home"),
    path('kitchen-dashboard/',kitchendashboard,name = "kitchen-dashboard"),
    path('kitchen-product/',kitchenDashboardProduct,name = "kitchen-product"),
    path('kitchen-page/<str:name>/', kitchenPage, name = "kitchenPage"),

    # Accounts URL
    path('customer-signup/',CustomerRegistration, name = "customer-signup"),
    path('kitchen-signup/',KitchenRegistration, name = "kitchen-signup"),
    path('login/',LoginProcess, name = "login-page"),
    path('logout/',LogoutProcess, name = "logout"),

    # MenuItem URL
    path('add-product/', AddProduct, name = "add-product"),
    path('edit-product/<int:id>/',editProduct, name = "edit-product"),
    path('delete-product/<int:id>/', deleteProduct, name = "delete-product"),

    path('cart/', new_cart, name = "cart"),
    path('update-item/', updateItem, name = "update-item"),
    path('checkout/', checkout, name = "checkout"),

    path('order-detail/', OrderDetail, name = "order-detail"),
    path('kitchen-order/', KitchenOrder, name = "kitchen-order"),
    path('update-order/', updateOrder, name = "update-order"),

    path('settings/', kitchenSetting, name = "setting"),
]
