from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'category', 'sent_at', 'is_read')
    list_filter = ('category', 'is_read')
    search_fields = ('name', 'email', 'message')
