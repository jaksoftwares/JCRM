from django.urls import path
from . import views

app_name = "prayers"

urlpatterns = [
    path('', views.prayer_request_list, name='prayer_requests'),
    path('submit/', views.submit_prayer_request, name='submit_prayer_request'),
    path('<int:pk>/', views.prayer_request_detail, name='prayer_request_detail'),
    path('<int:pk>/answered/', views.mark_prayer_as_answered, name='mark_prayer_as_answered'),
]
