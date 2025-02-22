from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path('', views.index, name='events'),
    path('', views.event_list, name='event_list'),
    path('<slug:slug>/', views.event_detail, name='event_detail'),
]
