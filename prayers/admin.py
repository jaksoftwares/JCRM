from django.contrib import admin
from .models import PrayerRequest, PrayerResponse

@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'visibility', 'is_approved', 'is_answered', 'created_at')
    list_filter = ('visibility', 'is_approved', 'is_answered')
    search_fields = ('title', 'name', 'email', 'request')
    actions = ['approve_requests', 'mark_as_answered']

    def approve_requests(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected requests have been approved.")

    def mark_as_answered(self, request, queryset):
        queryset.update(is_answered=True)
        self.message_user(request, "Selected requests have been marked as answered.")

@admin.register(PrayerResponse)
class PrayerResponseAdmin(admin.ModelAdmin):
    list_display = ('prayer_request', 'responder', 'created_at')
