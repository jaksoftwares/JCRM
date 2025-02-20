from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Speaker(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='speakers/', blank=True, null=True)

    def __str__(self):
        return self.name

class Sermon(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="sermons")
    speaker = models.ForeignKey(Speaker, on_delete=models.SET_NULL, null=True, related_name="sermons")
    video_url = models.URLField(blank=True, null=True)
    audio_file = models.FileField(upload_to='sermons/audio/', blank=True, null=True)
    sermon_notes = models.FileField(upload_to='sermons/notes/', blank=True, null=True)
    description = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)  # ✅ New field to mark featured sermons

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title