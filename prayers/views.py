from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import PrayerRequest, PrayerResponse
from .forms import PrayerRequestForm, PrayerResponseForm

def prayer_request_list(request):
    """Display approved public prayer requests."""
    requests = PrayerRequest.objects.filter(visibility='public', is_approved=True).order_by('-created_at')
    return render(request, 'prayers/prayer_requests.html', {'requests': requests})

def prayer_request_detail(request, pk):
    """View a specific prayer request and responses."""
    prayer_request = PrayerRequest.objects.get(pk=pk)
    responses = prayer_request.responses.all()
    form = PrayerResponseForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form = PrayerResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.prayer_request = prayer_request
            response.responder = request.user
            response.save()
            messages.success(request, "Your response has been added.")
            return redirect('prayer_request_detail', pk=pk)

    return render(request, 'prayers/prayer_request_detail.html', {'prayer_request': prayer_request, 'responses': responses, 'form': form})

@login_required
def submit_prayer_request(request):
    """Allow users to submit prayer requests."""
    form = PrayerRequestForm()

    if request.method == "POST":
        form = PrayerRequestForm(request.POST)
        if form.is_valid():
            prayer_request = form.save(commit=False)
            if request.user.is_authenticated:
                prayer_request.user = request.user
            prayer_request.save()
            messages.success(request, "Your prayer request has been submitted.")
            return redirect('prayer_requests')

    return render(request, 'prayers/submit_prayer_request.html', {'form': form})

@login_required
def mark_prayer_as_answered(request, pk):
    """Allow users or admins to mark a prayer request as answered."""
    prayer_request = PrayerRequest.objects.get(pk=pk)

    if prayer_request.user == request.user or request.user.is_staff:
        prayer_request.is_answered = True
        prayer_request.save()
        messages.success(request, "This prayer request has been marked as answered.")
    
    return redirect('prayer_requests')
