from django.urls import path
from . import views

app_name = "watch"

urlpatterns = [
    path('', views.index, name='watch'),
    path('', views.sermon_list, name='sermon_list'),
    path('<slug:slug>/', views.sermon_detail, name='sermon_detail'),
]
