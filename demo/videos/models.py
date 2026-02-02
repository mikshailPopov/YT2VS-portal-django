from django.db import models
from django.db.models.fields import return_None


class Video(models.Model):
    # name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, default="http://127.0.0.1:8000")
    date = models.DateTimeField("date published")

    def __str__(self):
        return self.url