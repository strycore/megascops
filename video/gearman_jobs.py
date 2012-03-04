import os
import json
import urllib
import urlparse
from subprocess import PIPE, Popen
from django_gearman.decorators import gearman_job
from django.template.defaultfilters import slugify
from gearman import GearmanClient

DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                         "../../videos/")


def get_video_info(url):
    vid_info_json, quvi_status = Popen(['quvi', url],
                                       stdout=PIPE,
                                       stderr=PIPE).communicate()
    vid_info = json.loads(vid_info_json)


def download_monitor(a, b, c):
    print "a", a
    print "b", b
    print "c", c


def download(url, dest_path, reporthook):
    print "Download in progress : %s" % url
    urllib.urlretrieve(flv_url, dest_path)


@gearman_job
def get_video_job(video):
    """Gearman job to download the video.

    The video parameter is an object of type Video, as defined in
    megascops.models.Video
    """
    vid_info = get_video_info(video.url)
    flv_url = vid_info['link'][0]['url']
    page_title = vid_info['page_title']
    filename = slugify(page_title) if page_title else "foo"
    dest_file = "%s.%s" % (filename,
                           vid_info['link'][0]['file_suffix'])
    dest_path = os.path.join(DATA_PATH, dest_file)
    download(flv_url, dest_path, download_monitor)
    video.state = "DOWNLOAD_FINISHED"


if __name__ == "__main__":
    url = "http://www.youtube.com/watch?v=nxhgP6xsrsY"
    fetch_video(url)
