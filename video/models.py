from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    """Profile associated with a user"""
    user = models.OneToOneField(User)
    size_quota = models.IntegerField(default=settings.DEFAULT_SIZE_QUOTA)
    video_quota = models.IntegerField(default=settings.DEFAULT_VIDEO_QUOTA)

    def __unicode__(self):
        return self.user.username


class Video(models.Model):
    """The video object"""
    user = models.ForeignKey(User)
    host = models.CharField(max_length=64, blank=True)
    title = models.CharField(max_length=256, blank=True)
    page_url = models.CharField(max_length=256)
    duration = models.IntegerField(default=0)
    filename = models.CharField(max_length=256)
    extension = models.CharField(max_length=10)
    state = models.CharField(max_length=24)
    thumbnail = models.FileField(upload_to='thumbnails', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % (self.title or self.page_url or self.id)

    @property
    def mimetype(self):
        return 'video/%s' % self.extension

    @property
    def path(self):
        return 'videos/%d-%s.%s' % (self.id, self.filename, self.extension)
