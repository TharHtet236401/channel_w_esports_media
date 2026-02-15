from django.db import models

from apps.core.constants import Region as RegionEnum

# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=200, choices=[(r.value, r.value) for r in RegionEnum])

    def __str__(self):
        return self.name

class Post(models.Model):
    caption = models.CharField(max_length=200)
    description = models.TextField()
    region = models.ManyToManyField(Region)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.caption
