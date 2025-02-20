from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ministry, MinistryMembership
from events.models import Event  # Importing events from the Events app
from .forms import MinistryMembershipForm


def index(request):
    return render(request, 'ministries/index.html')


def ministry_list(request):
    ministries = Ministry.objects.all()
    return render(request, 'ministries/ministry_list.html', {'ministries': ministries})

def ministry_detail(request, slug):
    ministry = get_object_or_404(Ministry, slug=slug)
    ministry_events = Event.objects.filter(category__name__icontains=ministry.name)
    return render(request, 'ministries/ministry_detail.html', {'ministry': ministry, 'events': ministry_events})

def join_ministry(request, slug):
    ministry = get_object_or_404(Ministry, slug=slug)
    
    if request.method == 'POST':
        form = MinistryMembershipForm(request.POST)
        if form.is_valid():
            membership = form.save(commit=False)
            membership.ministry = ministry
            membership.save()
            return redirect('ministry_detail', slug=ministry.slug)
    else:
        form = MinistryMembershipForm()

    return render(request, 'ministries/join_ministry.html', {'form': form, 'ministry': ministry})

