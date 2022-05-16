from django.db import models
from django.utils import timezone
# Create your models here.
class Result(models.Model):
    imagepath = models.TextField()
    image = models.ImageField(null=True, blank=True)
    predicted = models.TextField()
    confidence = models.IntegerField(default=0, null=True, blank=True)
    saved = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-saved',)

    def __str__(self):
        return self.imagepath
