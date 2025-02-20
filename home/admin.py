from django.contrib import admin
from .models import HeroSection

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Show title in the admin list
