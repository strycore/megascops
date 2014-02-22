import json
import logging
from urlparse import urlparse
import subprocess

LOGGER = logging.getLogger(__name__)


class Quvi(object):
    # TODO: handle '--print-streams' options to get all possible streams.
    # Note: this option does not retrieve video metadata

    def __init__(self, url=None):
        self._media = None
        self._streams = None
        self.url = url
        self.dump_type = None
        self.stream = None
        if self.url:
            self.get_media()

    def quvi_run(self, options):
        command = ['quvi', 'dump', '-p', 'json'] + options
        output = subprocess.Popen(command,
                                  stdout=subprocess.PIPE).communicate()[0]
        return json.loads(output)

    def get_streams(self, url):
        stream_data = self.quvi_run(['--print-streams', url])
        try:
            self._streams = stream_data['quvi']['media']['streams']
        except KeyError:
            LOGGER.warning('Unable to get streams from %s: %s',
                           url, stream_data)
            self._streams = []

    def get_media(self):
        media_data = self.quvi_run([self.url])
        try:
            self._media = media_data['quvi']['media']
            self.stream = QuviStream(self._media['stream'])
        except KeyError:
            LOGGER.warning("Unable to get media info from %s: %s",
                           self.url, media_data)
            self._media = {}

    @property
    def host(self):
        url_info = urlparse(self.url)
        return url_info.netloc

    @property
    def thumbnail_url(self):
        return self._media.get('QUVI_MEDIA_PROPERTY_THUMBNAIL_URL')

    @property
    def title(self):
        _title = self._media.get('QUVI_MEDIA_PROPERTY_TITLE')
        if not _title:
            return self.url

    @property
    def video_id(self):
        return self._media.get('QUVI_MEDIA_PROPERTY_ID')

    @property
    def duration(self):
        return self._media.get('QUVI_MEDIA_PROPERTY_DURATION_MS')


class QuviStream(object):
    def __init__(self, stream_data):
        self.stream = stream_data

    @property
    def extension(self):
        try:
            ext = self.stream['QUVI_HTTP_METAINFO_PROPERTY_FILE_EXTENSION']
        except KeyError:
            ext = self.stream['QUVI_MEDIA_STREAM_PROPERTY_CONTAINER']
        return ext

    @property
    def url(self):
        return self.stream['QUVI_MEDIA_STREAM_PROPERTY_URL']