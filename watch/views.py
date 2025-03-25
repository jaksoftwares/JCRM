from django.shortcuts import render, get_object_or_404
from .models import Sermon, Category


def index(request):
    video_ids = [
        "KzH9M7kDRKE?si=xcRU5bsXsQJZQ9IU",
        "kQ0VGJBoQNc?si=du565BVwTEPp86Ff",
        "Dc2mh-fjIpA?si=EpGaCn7QWltSanoJ",
        "czNxNxuxccs?si=F7OnNxqyB-IPjRmY",
        "ygKzxmn7Uj4?si=tlgUjReAHYUl0Uiz",
        "plXoL2J3yWA?si=DMFuaCDsmEsLkjdy",
        "gnoifsMTPTI?si=9tZfSgfW-pqQyQvr",
        "UGpUa6qW_K4?si=FJW73BoKz1YqrP6B",
        "YCHDK9aqr-4?si=ZcI2XKfRCp19tPz9",
        "uXE1SAdAfpg?si=f0QWpRykMZ2HCSOy",
        "nO4W0RwCbq4?si=Xuz08DB3s9QNO_N7",
        "AmboecR-hyI?si=mcJ9Qp1fOq2r3kS8",
    ]
    return render(request, "watch/index.html", {"video_ids": video_ids})


def sermon_list(request):
    categories = Category.objects.all()
    sermons = Sermon.objects.order_by("-publish_date")
    selected_category = request.GET.get("category")

    if selected_category:
        sermons = sermons.filter(category__slug=selected_category)

    context = {
        "categories": categories,
        "sermons": sermons,
        "selected_category": selected_category,
    }
    return render(request, "watch/sermon_list.html", context)


def sermon_detail(request, slug):
    sermon = get_object_or_404(Sermon, slug=slug)
    return render(request, "watch/sermon_detail.html", {"sermon": sermon})
