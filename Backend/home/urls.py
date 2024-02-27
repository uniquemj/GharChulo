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
    path('forgot-password/', ForgotPassword, name = "forgot-password"),
    path('change-forgot-password/<token>/', changeForgotPassword, name = "change-forgot-password"),
    path('logout/',LogoutProcess, name = "logout"),
    path('confirm-email/', verificationPage, name="verificationPage"),
    path('verified-account/', verifiedPage, name="verifiedPage"),
    path('kitchen-approval-pending/', approvalPending, name="approvalPending"),
    path('verify/<str:token>/', verify, name="verify"),

    # MenuItem URL
    path('product/<int:pk>/', productDetail, name = "product"),
    path('add-product/', AddProduct, name = "add-product"),
    path('edit-product/<int:id>/',editProduct, name = "edit-product"),
    path('delete-product/<int:id>/', deleteProduct, name = "delete-product"),

    path('cart/', new_cart, name = "cart"),
    path('update-item/', updateItem, name = "update-item"),
    path('checkout/', checkout, name = "checkout"),

    path('initiate/',initkhalti,name="initiate"),
    path('khalti-verify/', verifyKhalti, name="verify"),

    path('order-detail/', OrderDetail, name = "order-detail"),
    path('kitchen-order/', KitchenOrder, name = "kitchen-order"),
    path('update-order/', updateOrder, name = "update-order"),

    path('settings/', kitchenSetting, name = "setting"),
]
