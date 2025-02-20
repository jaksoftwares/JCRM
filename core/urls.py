from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),        
    path('sermons/', include('sermons.urls')),     
    path('blog/', include('blog.urls')),           
    path('donations/', include('donations.urls')), 
    path('users/', include('users.urls')),  
    path('', include('index.urls')),      

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
