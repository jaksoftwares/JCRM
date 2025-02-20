from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now

class EventCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, related_name="events")
    speaker = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    venue = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    registration_required = models.BooleanField(default=False)
    registration_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.event_date}"

    @staticmethod
    def upcoming_events():
        return Event.objects.filter(event_date__gte=now().date()).order_by('event_date')

    @staticmethod
    def recent_events():
        return Event.objects.filter(event_date__lt=now().date()).order_by('-event_date')[:5]

    @staticmethod
    def past_events():
        return Event.objects.filter(event_date__lt=now().date()).order_by('-event_date')
