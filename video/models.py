from django.db import models


class Video(models.Model):
    host = models.CharField(max_length=64, blank=True, null=True)
    page_title = models.CharField(max_length=256, blank=True, null=True)
    page_url = models.CharField(max_length=256)
    #content_type = models.CharField(max_length=64)
    #file_suffix = models.CharField(max_length=8)
    filename = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=24)

    def __unicode__(self):
        return "[%s] %s" %(self.state, self.page_url)
