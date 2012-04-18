import os
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

import settings

from registration.signals import user_registered

class Profile(models.Model):
    user = models.OneToOneField(User)
    size_quota = models.IntegerField(default=settings.DEFAULT_SIZE_QUOTA)
    video_quota = models.IntegerField(default=settings.DEFAULT_VIDEO_QUOTA)

    def __unicode__(self):
        return self.user.username


class VideoManager(models.Manager):
    def get_query_set(self):
        return super(VideoManager, self).get_query_set().filter(
                state__in=["READY", "DOWNLOAD_FINISHED"]
            )

class Video(models.Model):
    profile = models.ForeignKey(Profile)
    host = models.CharField(max_length=64, blank=True, null=True)
    page_title = models.CharField(max_length=256, blank=True, null=True)
    page_url = models.CharField(max_length=256)
    duration = models.IntegerField(default=0)
    filename = models.CharField(max_length=256)
    file_suffix = models.CharField(max_length=10)
    state = models.CharField(max_length=24)
    thumbnail = models.FileField(upload_to=os.path.join(settings.MEDIA_ROOT,
                                                        'thumbnails/'), 
                                 null=True)
    progress = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)

    objects = models.Manager()
    ready = VideoManager()

    def __unicode__(self):
        return "[%s] %s" % (self.state, self.page_url)

def user_created(sender, user, request, **kwargs):
    profile, created = Profile.objects.get_or_create(user=user)
    profile.save()
user_registered.connect(user_created, dispatch_uid="video.models.user_created")
