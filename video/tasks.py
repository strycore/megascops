# -*- coding: utf8 -*-
from __future__ import absolute_import
import os
import logging

from datetime import datetime
from celery import task

from django.template.defaultfilters import slugify
from django.conf import settings

from video.models import Video
from video.utils import (get_streams, download_thumbnail, VideoDownloader,
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
    vid_info = get_streams(video.page_url)
    page_title = (
        vid_info['pagetitle']
        if vid_info['pagetitle']
        else "%s video %s" % (vid_info['hostid'], str(datetime.now()))
    )
    video.page_title = page_title
    video.host = vid_info['hostid']

    flv_url = vid_info['mediaurl']
    filename = slugify(page_title)
    video.filename = filename
    video.duration = vid_info['mediaduration']
    video.file_suffix = vid_info['filesuffix']
    dest_file = "%s.%s" % (filename, vid_info['filesuffix'])
    dest_path = os.path.join(settings.MEDIA_ROOT, 'video/', dest_file)
    if vid_info['mediathumbnail']:
        video.thumbnail = download_thumbnail(vid_info)
    video.state = "DOWNLOAD_STARTED"
    video.save()
    downloader = VideoDownloader(video_id)
    downloader.download(flv_url, dest_path)
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
