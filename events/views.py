from django.shortcuts import render, get_object_or_404
from .models import Event, EventCategory
from datetime import date


def index(request):
    def buildImageUrl(path:str)->str:
        baseUrl = "images/events"
        return "{baseUrl}/{path}".format(baseUrl=baseUrl,path=path)

    events = [
        {
            "title":"Healing & Deliverance Crusade",
            "description":"Our recent Healing & Deliverance Crusade was a night of breakthroughs! Many experienced the power of God through healing, deliverance, and prophetic ministration. Testimonies of restoration and renewed faith filled the atmosphere as we witnessed God move mightily.",
            "date":"JAN 22",
            "image_url":buildImageUrl("event1.png")
        },
        {
            "title":"Christmas Worship Celebration",
            "description":"The Christmas Worship Celebration was an unforgettable moment of joy, praise, and gratitude. Families and friends gathered to celebrate the birth of Christ through powerful worship, scripture readings, and acts of love within the community.",
            "date":"DEC 25",
            "image_url":buildImageUrl("event2.png")
        },
        {
            "title":"21 Days of Prayer & Fasting",
            "description":"Our 21 Days of Prayer & Fasting brought the congregation closer to God as we sought His will for the new season. The testimonies of spiritual renewal, answered prayers, and divine direction have been truly inspiring.",
            "date":"JAN 22",
            "image_url":buildImageUrl("event3.png"),
            "is_ongoing":True,
        },
        {
            "title":"Healing & Deliverance Crusade",
            "description":"Our recent Healing & Deliverance Crusade was a night of breakthroughs! Many experienced the power of God through healing, deliverance, and prophetic ministration. Testimonies of restoration and renewed faith filled the atmosphere as we witnessed God move mightily.",
            "date":"FEB 13",
            "image_url":buildImageUrl("event4.png")
        },
    ]
    return render(request, 'events/index.html',{"events":events})

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
