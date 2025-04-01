from django.shortcuts import render
from .models import HeroSection
from watch.models import Sermon
from events.models import Event
from ministries.models import Ministry

def home_page(request):
    featured_sermons = Sermon.objects.filter(featured=True).order_by('-publish_date')[:3]  
    upcoming_events = Event.upcoming_events()[:3]  
    recent_events = Event.recent_events()[:3]  
    past_events = Event.past_events()[:3]  
    ministries = Ministry.objects.all()[:4]
    context = {
        'featured_sermons': featured_sermons,
        'upcoming_events': upcoming_events,
        'ministries': ministries,
    }
    return render(request, 'home/index.html', context)