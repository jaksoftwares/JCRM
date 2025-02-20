from django.db import models

class HeroSection(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField(blank=True, null=True)
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    
    def __str__(self):
        return self.title
