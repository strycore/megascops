import os
import json
import urllib
import urlparse
import datetime
from subprocess import PIPE, Popen
from django_gearman.decorators import gearman_job
from django.template.defaultfilters import slugify
from gearman import GearmanClient
from megascops.video.models import Video

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         "../../videos/"))
print "Saving videos in %s" % DATA_PATH
global VIDEO_ID
VIDEO_ID = 999


def get_video_info(url):
    vid_info_json, quvi_status = Popen(['quvi', url],
                                       stdout=PIPE,
                                       stderr=PIPE).communicate()
    print vid_info_json
    print quvi_status
    vid_info = json.loads(vid_info_json)
    return vid_info


class Downloader(object):
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
        VIDEO_ID = video_id
        print "Starting download of video %s" % VIDEO_ID
        video = Video.objects.get(pk=video_id)
        video.state = "FETCHING_INFO"
        video.save()
        vid_info = get_video_info(video.page_url)
        page_title = vid_info['page_title'] if vid_info['page_title'] \ 
                     else "%s video %s" % (vid_info['host'],
                                           str(datetime.now()))
        video.page_title = 'page_title'
        video.host = vid_info['host']

        flv_url = vid_info['link'][0]['url']
        filename = slugify(page_title)
        video.filename = filename
        video.save()
        dest_file = "%s.%s" % (filename,
                               vid_info['link'][0]['file_suffix'])
        dest_path = os.path.join(DATA_PATH, dest_file)
        video.state = "DOWNLOAD_STARTED"
        video.save()
        downloader = Downloader(video_id)
        downloader.download(flv_url, dest_path)
        video.state = "DOWNLOAD_FINISHED"
        video.save()
    except Exception, e:
        print e


if __name__ == "__main__":
    url = "http://www.youtube.com/watch?v=nxhgP6xsrsY"
    info = get_video_info(url)
    print info
