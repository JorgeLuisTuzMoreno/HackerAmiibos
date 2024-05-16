from django.db import models
from django.conf import settings

class Amiibo(models.Model):
    url = models.URLField()
    name = models.TextField(blank=True)
    amiiboserie = models.TextField(blank=True)
    gameseries = models.TextField(blank=True)
    type = models.TextField(blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    link = models.ForeignKey('links.Amiibo', related_name='votes', on_delete=models.CASCADE)
