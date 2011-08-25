from django.db import models

class Video(models.Model):
    host = models.CharField(max_length=64)
    page_title = models.CharField(max_length=256)
    page_url = models.CharField(max_length=256)
    content_type = models.CharField(max_length=64)
    file_suffix = models.CharField(max_length=8)
    filename=models.CharField(max_length=128)

