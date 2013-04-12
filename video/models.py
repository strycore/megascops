"""Video models"""
import os
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from registration.signals import user_registered


class Profile(models.Model):
    """Profile associated with a user"""
    user = models.OneToOneField(User)
    size_quota = models.IntegerField(default=settings.DEFAULT_SIZE_QUOTA)
    video_quota = models.IntegerField(default=settings.DEFAULT_VIDEO_QUOTA)

    def __unicode__(self):
        return self.user.username

    def viewable_videos(self):
        return self.video_set.ready()

    def unviewable_videos(self):
        return self.video_set.pending()


class VideoManager(models.Manager):
    def ready(self):
        return self.get_query_set().filter(
            state__in=["READY", "DOWNLOAD_FINISHED"]
        )

    def pending(self):
        return self.get_query_set().exclude(
            state__in=["READY", "DOWNLOAD_FINISHED"]
        )


class Video(models.Model):
    """The video object"""
    profile = models.ForeignKey(Profile)
    host = models.CharField(max_length=64, blank=True, null=True)
    page_title = models.CharField(max_length=256, blank=True, null=True)
    page_url = models.CharField(max_length=256)
    duration = models.IntegerField(default=0)
    filename = models.CharField(max_length=256)
    file_suffix = models.CharField(max_length=10)
    state = models.CharField(max_length=24)
    thumbnail = models.FileField(upload_to='thumbnails', null=True)
    progress = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)

    objects = VideoManager()

    def __unicode__(self):
        return "%s" % (self.page_title or self.page_url or self.id)

    def has_file_format(self, file_format):
        return os.path.exists(os.path.join(
            settings.MEDIA_ROOT, "video", self.filename + "." + file_format
        ))

    @property
    def has_webm(self):
        return self.has_file_format("webm")

    @property
    def has_mp4(self):
        return self.has_file_format("mp4")


def user_created(sender, user, request, **kwargs):
    profile, created = Profile.objects.get_or_create(user=user)
    profile.save()
user_registered.connect(user_created, dispatch_uid="video.models.user_created")
