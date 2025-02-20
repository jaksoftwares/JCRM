from django.contrib import admin
from .models import Sermon, Category, Speaker

admin.site.register(Category)
admin.site.register(Speaker)
admin.site.register(Sermon)
