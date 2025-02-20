from django.shortcuts import render, get_object_or_404
from .models import Event, EventCategory
from datetime import date


def index(request):
    return render(request, 'events/index.html')

def event_list(request):
    categories = EventCategory.objects.all()
    upcoming_events = Event.objects.filter(event_date__gte=date.today()).order_by("event_date")
    past_events = Event.objects.filter(event_date__lt=date.today()).order_by("-event_date")
    
    selected_category = request.GET.get('category')
    if selected_category:
        upcoming_events = upcoming_events.filter(category__slug=selected_category)
        past_events = past_events.filter(category__slug=selected_category)

    context = {
        'categories': categories,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'selected_category': selected_category,
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'events/event_detail.html', {'event': event})
