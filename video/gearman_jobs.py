import os
import json
import urllib
import urlparse
from subprocess import PIPE, Popen
from django_gearman.decorators import gearman_job
from django.template.defaultfilters import slugify
from gearman import GearmanClient
from megascops.video.models import Video

DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                         "../../videos/")
CURRENT_VIDEO = None


def get_video_info(url):
    vid_info_json, quvi_status = Popen(['quvi', url],
                                       stdout=PIPE,
                                       stderr=PIPE).communicate()
    vid_info = json.loads(vid_info_json)
    return vid_info


def download_monitor(piece, block_size, total_size):
    bytes_downloaded = piece * block_size
    print "%d / %d " % (bytes_downloaded, total_size)


def download(url, dest_path):
    urllib.urlretrieve(url, dest_path, download_monitor)


@gearman_job
def get_video_job(video_id):
    """Gearman job to download the video.

    The video parameter is an object of type Video, as defined in
    megascops.models.Video
    """
    video = Video.objects.get(pk=video_id)
    CURRENT_VIDEO = video
    vid_info = get_video_info(video.page_url)
    flv_url = vid_info['link'][0]['url']
    page_title = vid_info['page_title']
    filename = slugify(page_title) if page_title else "foo"
    video.filename = filename
    video.save()
    dest_file = "%s.%s" % (filename,
                           vid_info['link'][0]['file_suffix'])
    dest_path = os.path.join(DATA_PATH, dest_file)
    video.state = "DOWNLOAD_STARTED"
    video.save()
    download(flv_url, dest_path)
    video.state = "DOWNLOAD_FINISHED"
    video.save()


if __name__ == "__main__":
    url = "http://www.youtube.com/watch?v=nxhgP6xsrsY"
    fetch_video(url)
