import os
import uuid
import urllib
from urlparse import urlparse
import subprocess
from django.conf import settings
from video.models import Video


def sanitize_url(url):
    """ Make sure an url is valid, prepending the scheme if needed. """
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "http://" + url
    parsed = urlparse(url)
    if not '.' in parsed.netloc:
        raise ValueError("Invalid url %s" % url)
    return url


def download_thumbnail(thumbnail_url):
    destination_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    thumbnail_file = str(uuid.uuid4()) + ".jpg"
    urllib.urlretrieve(thumbnail_url, os.path.join(destination_path,
                                                   thumbnail_file))
    thumb_rel_path = os.path.join('thumbnails', thumbnail_file)
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
    subprocess.Popen(cmd % params, shell=True).communicate()


# pylint: disable=R0903
class CeleryDownloader(object):
    """ Download a file and report progress to a Celery task. """
    def __init__(self, caller):
        self.caller = caller

    def monitor_progress(self, piece, block_size, total_size):
        bytes_downloaded = piece * block_size
        if total_size:
            progress = bytes_downloaded / (total_size * 1.0)
        else:
            progress = 0
        percent = int(progress * 100)
        self.caller.update_state(state='PROGRESS',
                                 meta={'percent': percent})

    def download(self, url, dest_path):
        urllib.urlretrieve(url, dest_path, self.monitor_progress)
