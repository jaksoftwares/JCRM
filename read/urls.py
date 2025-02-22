app_name = "read"

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='read'),
]
