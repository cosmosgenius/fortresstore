from django.db import models
from taggit.managers import TaggableManager


class App(models.Model):
    app_id = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    description = models.TextField()
    developer_name = models.CharField(max_length=500)
    developer_email = models.EmailField(null=True)
    developer_url = models.URLField()
    price = models.DecimalField(decimal_places=4, max_digits=10)
    rating = models.DecimalField(decimal_places=2, max_digits=5)
    cover_large = models.ImageField()
    cover_small = models.ImageField()
    url = models.URLField()

    tags = TaggableManager()
