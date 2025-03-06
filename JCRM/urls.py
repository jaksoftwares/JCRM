from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs with Namespaces
    path('', include('home.urls', namespace='home')),
    path('about/', include('about.urls', namespace='about')),
    path('watch/', include('watch.urls', namespace='watch')),
    path('read/', include('read.urls', namespace='read')),
    path('listen/', include('listen.urls', namespace='listen')),
    path('ministries/', include('ministries.urls', namespace='ministries')),
    path('events/', include('events.urls', namespace='events')),
    path('store/', include('store.urls', namespace='store')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('account/', include('account.urls', namespace='account')),
    path('prayers/', include('prayers.urls', namespace='prayers')),
    path('donations/', include('donations.urls', namespace='donations')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('resources/', include('resources.urls', namespace='resources')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


