import os
import json
import urllib
import urlparse
import datetime
from subprocess import PIPE, Popen
from django_gearman.decorators import gearman_job
from django.template.defaultfilters import slugify
from django_gearman import GearmanClient, Task
from quvi import Quvi
from video.models import Video
import settings


def get_video_info(url):
    quvi = Quvi()
    quvi.parse(url)
    vid_info = quvi.get_properties()
    return vid_info


class VideoDownloader(object):
    def __init__(self, video_id):
        self.video_id = video_id
        self.video = Video.objects.get(pk=video_id)

    def _download_monitor(self, piece, block_size, total_size):
        bytes_downloaded = piece * block_size
        progress = bytes_downloaded / (total_size * 1.0)
        print "%d / %d " % (bytes_downloaded, total_size)
        if piece % 100 == 0:
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
    print "job launched"
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
        video.file_suffix = vid_info['filesuffix']
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

        # Launch video encoding
        client = GearmanClient()
        client.dispatch_background_task('video.encode', video.id)

    except Exception, e:
        print "error"
        print e

@gearman_job
def encode(video_id):
    """Encode video using avconv"""
    print "convert in progress"
    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        print "The requested video does not exist"
        return

    try:
        path_format = "%s/video/%s.%s"
        orig_file = path_format % (settings.MEDIA_ROOT, 
                                video.filename, video.file_suffix)
        mp4_file = path_format % (settings.MEDIA_ROOT, 
                                video.filename, "mp4")
        webm_file = path_format % (settings.MEDIA_ROOT, 
                                video.filename, "webm")

        cmd = "avconv -i %(input)s %(codec)s %(options)s %(output)s"
        if orig_file != webm_file:
            if os.path.exists(webm_file):
                os.remove(webm_file)
            params = {"input": orig_file, "output": webm_file, 
                      "codec": "-vcodec libvpx -acodec libvorbis",
                      "options": "-b:v 1250k -qmax 63 -b:a 56k -ar 22050"}
            print cmd % params
            Popen(cmd % params, shell=True).communicate()
        if orig_file != mp4_file:
            if os.path.exists(mp4_file):
                os.remove(mp4_file)
            params = {"input": orig_file, "output": mp4_file,
                      "codec": "", "options": ""}
            print cmd % params
            Popen(cmd % params, shell=True).communicate()
    except Exception, e:
        print "convert error"
        print e


def main():
    url = "http://www.youtube.com/watch?v=nxhgP6xsrsY"
    info = get_video_info(url)
    print info

if __name__ == "__main__":
    main()
