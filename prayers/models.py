from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class PrayerRequest(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public (Visible to All)'),
        ('private', 'Private (Only Admins See)'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)  # For anonymous requests
    email = models.EmailField(blank=True, null=True)
    title = models.CharField(max_length=255)
    request = models.TextField()
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    is_approved = models.BooleanField(default=False)  # Admin approval for public requests
    is_answered = models.BooleanField(default=False)  # Marked if prayer is answered
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.title} - {self.get_visibility_display()}"

class PrayerResponse(models.Model):
    prayer_request = models.ForeignKey(PrayerRequest, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    response = models.TextField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Response by {self.responder.username if self.responder else 'Anonymous'}"
