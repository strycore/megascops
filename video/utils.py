import os
import urllib
from quvi import get_properties_best_quality  # , Quvi
from subprocess import Popen
from django.conf import settings
from video.models import Video


def get_video_info(url):
    #quvi = Quvi()
    #quvi.parse(url)
    #vid_info = quvi.get_properties()
    #return vid_info
    return get_properties_best_quality(url)


def download_thumbnail(vid_info):
    thumbnail = "%s%s.jpg" % (vid_info['hostid'], vid_info['mediaid'])
    thumb_rel_path = os.path.join('thumbnails/', thumbnail)
    thumb_path = os.path.join(settings.MEDIA_ROOT, thumb_rel_path)
    urllib.urlretrieve(vid_info['mediathumbnail'], thumb_path)
    return thumb_rel_path


def encode_videos(video):
    path_format = "%s/video/%s.%s"
    orig_file = path_format % (settings.MEDIA_ROOT,
                               video.filename, video.file_suffix)
    mp4_file = path_format % (settings.MEDIA_ROOT,
                              video.filename, "mp4")
    webm_file = path_format % (settings.MEDIA_ROOT,
                               video.filename, "webm")

    if orig_file != webm_file:
        launch_encoder(orig_file, webm_file)
    if orig_file != mp4_file:
        launch_encoder(orig_file, mp4_file)


def launch_encoder(input_file, output_file, codec="", options=""):
    cmd = "avconv -i %(input)s %(codec)s %(options)s %(output)s"
    if os.path.exists(output_file):
        os.remove(output_file)
    params = {"input": input_file, "output": output_file,
              "codec": codec, "options": options}
    #print cmd % params
    Popen(cmd % params, shell=True).communicate()


class VideoDownloader(object):
    def __init__(self, video_id):
        self.video_id = video_id
        self.video = Video.objects.get(pk=video_id)

    def _download_monitor(self, piece, block_size, total_size):
        bytes_downloaded = piece * block_size
        progress = bytes_downloaded / (total_size * 1.0)
        #print "%d / %d " % (bytes_downloaded, total_size)
        if piece % 100 == 0:
            self.video.progress = progress * 100
            self.video.save()

    def download(self, url, dest_path):
        urllib.urlretrieve(url, dest_path, self._download_monitor)
