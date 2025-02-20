from django.db import models
from django.utils.timezone import now

class ContactMessage(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General Inquiry'),
        ('prayer', 'Prayer Request'),
        ('support', 'Technical Support'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    message = models.TextField()
    sent_at = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.category}"
