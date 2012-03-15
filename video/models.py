from django.db import models
import settings
import os


class Video(models.Model):
    host = models.CharField(max_length=64, blank=True, null=True)
    page_title = models.CharField(max_length=256, blank=True, null=True)
    page_url = models.CharField(max_length=256)
    duration = models.IntegerField(default=0)
    filename = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=24)
    thumbnail = models.FileField(upload_to=os.path.join(settings.MEDIA_ROOT,
                                                        'thumbnails/'))
    progress = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return "[%s] %s" % (self.state, self.page_url)
