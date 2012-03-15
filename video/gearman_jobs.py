import os
import json
import urllib
import urlparse
import datetime
from subprocess import PIPE, Popen
from django_gearman.decorators import gearman_job
from django.template.defaultfilters import slugify
from gearman import GearmanClient
from quvi import Quvi
from megascops.video.models import Video
import settings


def get_video_info(url):
    vid_info_json, quvi_status = Popen(['quvi', url],
                                       stdout=PIPE,
                                       stderr=PIPE).communicate()
    quvi = Quvi()
    quvi.parse(url)
    vid_info = quvi.getproperties()
    return vid_info


class VideoDownloader(object):
    def __init__(self, video_id):
        self.video_id = video_id
        self.video = Video.objects.get(pk=video_id)

    def _download_monitor(self, piece, block_size, total_size):
        bytes_downloaded = piece * block_size
        progress = bytes_downloaded / (total_size * 1.0)
        print "%d / %d " % (bytes_downloaded, total_size)
        if piece % 25 == 0:
            self.video.progress = progress
            self.video.save()

    def download(self, url, dest_path):
        urllib.urlretrieve(url, dest_path, self._download_monitor)


@gearman_job
def get_video_job(video_id):
    """Gearman job to download the video.

    The video parameter is an object of type Video, as defined in
    megascops.models.Video
    """
    try:
        print "Starting download of video %s" % video_id
        video = Video.objects.get(pk=video_id)
        video.state = "FETCHING_INFO"
        video.save()
        vid_info = get_video_info(video.page_url)
        page_title = vid_info['pagetitle'] if vid_info['pagetitle']\
                     else "%s video %s" % (vid_info['hostid'],
                                           str(datetime.now()))
        video.page_title = page_title
        video.host = vid_info['hostid']

        flv_url = vid_info['mediaurl']
        filename = slugify(page_title)
        video.filename = filename
        video.duration = vid_info['mediaduration']
        dest_file = "%s.%s" % (filename,
                               vid_info['filesuffix'])
        dest_path = os.path.join(settings.MEDIA_ROOT, 'video/', dest_file)
        thumbnail = "%s%s.jpg" % (vid_info['hostid'], vid_info['mediaid'])
        video.thumbnail = thumbnail
        thumb_path = os.path.join(settings.MEDIA_ROOT,
                                  'thumbnails/', thumbnail)
        urllib.urlretrieve(vid_info['mediathumbnail'], thumb_path)
        video.state = "DOWNLOAD_STARTED"
        video.save()

        downloader = VideoDownloader(video_id)
        downloader.download(flv_url, dest_path)
        video.state = "DOWNLOAD_FINISHED"
        video.save()
    except Exception, e:
        print "error"
        print e


if __name__ == "__main__":
    url = "http://www.youtube.com/watch?v=nxhgP6xsrsY"
    info = get_video_info(url)
    print info
