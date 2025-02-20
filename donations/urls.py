app_name = "donations"

from django.urls import path
from . import views

urlpatterns = [
     path('', views.donate, name='donate'),
    path("donate/", views.donate, name="donate"),
    path("donation-success/", views.donation_success, name="donation_success"),
    path("paypal-success/", views.paypal_success, name="paypal_success"),
    path("history/", views.donation_history, name="donation_history"),
    path("<int:donation_id>/", views.donation_detail, name="donation_detail"),
]
