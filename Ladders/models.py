from django.db import models

class Event(models.Model):
    event_id = models.CharField(max_length=64)
    source = models.CharField(max_length=64)
    dest = models.CharField(max_length=64)
    time_stamp = models.DateTimeField('')
    summary = models.CharField(max_length=256)
    detail = models.CharField(max_length=20000)

# Create your models here.
