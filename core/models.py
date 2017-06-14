from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class Developer(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=500)
    url = models.URLField()


class App(models.Model):
    app_id = models.CharField(max_length=500, unique=True)
    name = models.CharField(max_length=500)
    description = models.TextField()
    price = models.DecimalField(decimal_places=4, max_digits=10)
    rating = models.DecimalField(decimal_places=2, max_digits=5)
    cover_large = models.ImageField()
    cover_small = models.ImageField()
    url = models.URLField()

    developer = models.ForeignKey(Developer, related_name='apps')

    tags = TaggableManager()

    def get_absolute_url(self):
        return '{}?id={}'.format(
            reverse('app-detail'),
            self.app_id
        )


class Screenshot(models.Model):
    url = models.URLField()
    app = models.ForeignKey(App, related_name='screenshots')
