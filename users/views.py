from django.shortcuts import render

def login_view(request):
    return render(request, 'users/login.html')

def logout_view(request):
    return render(request, 'users/logout.html')

def register_view(request):
    return render(request, 'users/register.html')

def profile_view(request):
    return render(request, 'users/profile.html')
