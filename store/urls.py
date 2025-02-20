from django.urls import path
from . import views
from .views import download_purchases, mpesa_webhook, paypal_webhook, stripe_webhook

app_name = "store"

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/', views.initiate_payment, name='checkout'),
    path('webhook/mpesa/', mpesa_webhook, name='mpesa_webhook'),
    path('webhook/paypal/', paypal_webhook, name='paypal_webhook'),
    path('webhook/stripe/', stripe_webhook, name='stripe_webhook'),
    path('downloads/', download_purchases, name='download_purchases'),
]
