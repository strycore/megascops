# -*- coding: utf8 -*-
from __future__ import absolute_import
import os
import logging

from celery import task, current_task

from django.conf import settings

from .models import Video
from .quvi import Quvi
from .utils import download_thumbnail, celery_download, encode_videos

LOGGER = logging.getLogger(__name__)


@task
def fetch_video(quvi_dump, video_id):
    """ Task to download the video.

        The video parameter is an object of type Video, as defined in
        megascops.models.Video
    """
    quvi = Quvi(dump=quvi_dump)
    video = Video.objects.get(pk=video_id)
    if quvi.thumbnail_url:
        video.thumbnail = download_thumbnail(quvi.thumbnail_url)

    dest_path = os.path.join(settings.MEDIA_ROOT, video.path)
    celery_download(quvi.stream.url, dest_path, current_task)
    video.state = "READY"
    video.save()


@task
def encode_task(video_id):
    """Encode video using avconv"""
    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        print "The requested video does not exist"
        return
    encode_videos(video)
