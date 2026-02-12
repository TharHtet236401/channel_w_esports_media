from django.db import models

# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=200)

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
