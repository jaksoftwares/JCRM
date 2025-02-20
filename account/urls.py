app_name = "account"

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='account-index'),
]
