app_name = "ministries"

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.ministry_list, name='ministry_list'),
    path('<slug:slug>/', views.ministry_detail, name='ministry_detail'),
    path('<slug:slug>/join/', views.join_ministry, name='join_ministry'),
]
