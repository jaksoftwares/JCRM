app_name = "about"

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='about'),
]
