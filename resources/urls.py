from django.urls import path
from . import views

app_name = "resources"


urlpatterns = [
    path('', views.resources, name='resources'),
]