from django.shortcuts import render, get_object_or_404
from .models import Sermon, Category

def index(request):
    return render(request, 'watch/index.html')

def sermon_list(request):
    categories = Category.objects.all()
    sermons = Sermon.objects.order_by('-publish_date')
    selected_category = request.GET.get('category')

    if selected_category:
        sermons = sermons.filter(category__slug=selected_category)

    context = {
        'categories': categories,
        'sermons': sermons,
        'selected_category': selected_category,
    }
    return render(request, 'watch/sermon_list.html', context)

def sermon_detail(request, slug):
    sermon = get_object_or_404(Sermon, slug=slug)
    return render(request, 'watch/sermon_detail.html', {'sermon': sermon})

