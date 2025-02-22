app_name = "listen"

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='listen'),
]
