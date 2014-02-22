# -*- coding: utf8 -*-
from __future__ import absolute_import
import os
import logging

from celery import task

from django.template.defaultfilters import slugify
from django.conf import settings

from video.models import Video
from .quvi import Quvi
from video.utils import (download_thumbnail, VideoDownloader,
                         encode_videos)

LOGGER = logging.getLogger(__name__)


@task
def fetch_video(video_id):
    """Task to download the video.

    The video parameter is an object of type Video, as defined in
    megascops.models.Video """
    video = Video.objects.get(pk=video_id)
    LOGGER.info("Fetching %s", video)
    video.state = "FETCHING_INFO"
    video.save()
    quvi = Quvi(video.page_url)
    video.page_title = quvi.title
    video.host = quvi.host

    video.filename = slugify(quvi.title)
    video.duration = quvi.duration
    video.file_suffix = quvi.stream.extension
    dest_file = "%s.%s" % (video.filename, quvi.stream.extension)
    dest_path = os.path.join(settings.MEDIA_ROOT, 'videos/', dest_file)
    if quvi.thumbnail_url:
        video.thumbnail = download_thumbnail(quvi.thumbnail_url)
    video.state = "DOWNLOAD_STARTED"
    video.save()
    downloader = VideoDownloader(video_id)
    downloader.download(quvi.stream.url, dest_path)
    video.state = "DOWNLOAD_FINISHED"
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
