from django.db import models
from django.utils import timezone
# Create your models here.
class Result(models.Model):
    imagepath = models.TextField()
    imagelink = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True)
    predicted = models.TextField()
    confidence = models.IntegerField(default=0, null=True, blank=True)
    saved = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-saved',)

    def __str__(self):
        return self.imagepath


class APIResult(models.Model):
    imagename = models.TextField(null=True)
    imagelink = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True)
    predicted = models.TextField()
    confidence = models.IntegerField(default=0, null=True, blank=True)
    saved = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.imagename
