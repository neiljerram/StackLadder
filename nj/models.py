from django.db import models

# Create your models here.

class NJRecord(models.Model):
    event_id = models.CharField(max_length=64)
    source = models.CharField(max_length=64)
    dest = models.CharField(max_length=64)
    time_stamp = models.DateTimeField('')
    summary = models.CharField(max_length=256)
    detail = models.CharField(max_length=20000)

class Record2(models.Model):
    event_id = models.CharField(max_length=64)
    src_ip = models.CharField(max_length=16)
    dst_ip = models.CharField(max_length=16)
    src_port = models.CharField(max_length=6)
    dst_port = models.CharField(max_length=6)
    src_name = models.CharField(max_length=32)
    dst_name = models.CharField(max_length=32)
    time_stamp = models.DateTimeField('')
    summary = models.CharField(max_length=256)
    detail = models.CharField(max_length=20000)

class MD4Record(models.Model):
    event_id = models.CharField(max_length=64)
    src_ip = models.CharField(max_length=16)
    dst_ip = models.CharField(max_length=16)
    src_port = models.CharField(max_length=6)
    dst_port = models.CharField(max_length=6)
    src_name = models.CharField(max_length=32)
    dst_name = models.CharField(max_length=32)
    time_stamp = models.DateTimeField('')
    summary = models.CharField(max_length=256)
    detail = models.CharField(max_length=20000)
