from django.shortcuts import render

def resources(request):
 
    return render(request, 'resources/index.html')