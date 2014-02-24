import os
import uuid
import logging
import requests
from urlparse import urlparse
import subprocess
from django.conf import settings

LOGGER = logging.getLogger(__name__)


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
    thumbnail_filename = str(uuid.uuid4()) + ".jpg"
    response = requests.get(thumbnail_url)
    thumbnail_path = os.path.join(destination_path, thumbnail_filename)
    with open(thumbnail_path, 'w') as thumbnail_file:
        thumbnail_file.write(response.content)
    thumb_rel_path = os.path.join('thumbnails', thumbnail_filename)
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


def celery_download(url, dest_path, caller):
    """ Download a file and report progress to a Celery task. """
    headers = {
        'User-agent': 'Mozilla/5.0 '
                      '(X11; Ubuntu; Linux x86_64; rv:27.0) '
                      'Gecko/20100101 Firefox/27.0'
    }
    response = requests.get(url, headers=headers)
    if response.status_code > 400:
        LOGGER.warning("Unable to get valid response for %s (status %s)",
                       url, response.status_code)
        return
    total_size = int(response.headers['Content-Length'])
    bytes_downloaded = 0.0
    with open(dest_path, 'wb') as dest_file:
        chunk_size = 1024
        for buf in response.iter_content(chunk_size):
            if buf:
                dest_file.write(buf)
                bytes_downloaded += chunk_size
                percent = int((bytes_downloaded / (total_size)) * 100)
                caller.update_state(state='PROGRESS',
                                    meta={'percent': percent})
