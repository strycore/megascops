import json
import logging
from urlparse import urlparse
import urllib
import subprocess

LOGGER = logging.getLogger(__name__)


class Quvi(object):
    # TODO: handle '--print-streams' options to get all possible streams.
    # Note: this option does not retrieve video metadata

    def __init__(self, url=None, dump=None):
        self._media = None
        self._streams = None
        self._playlist = None
        self.url = url
        self.raw_dump = dump
        self.dump_type = None
        self.stream = None
        if self.url:
            self.raw_dump = self.quvi_run([self.url])
            self.raw_dump['url'] = self.url
        else:
            self.raw_dump = json.loads(dump)
            self.url = self.raw_dump['url']
        self.parse_dump()

    def __repr__(self):
        return "<Quvi url=%s type=%s>" % (self.url, self.dump_type)

    @staticmethod
    def quvi_run(options):
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

    def parse_dump(self):
        if 'error' in self.raw_dump:
            raise QuviError(self.raw_dump['error'])
        if not 'quvi' in self.raw_dump:
            raise ValueError("Invalid response from quvi: %s", self.raw_dump)
        if 'media' in self.raw_dump['quvi']:
            self.dump_type = 'MEDIA'
            self._media = self.raw_dump['quvi']['media']
            self.stream = QuviStream(self._media['stream'])
        elif 'playlist' in self.raw_dump['quvi']:
            self.dump_type = 'PLAYLIST'
            self._playlist = self.raw_dump['quvi']['playlist']

    @property
    def dump(self):
        if self.dump_type == 'PLAYLIST':
            return self._playlist
        elif self.dump_type == 'MEDIA':
            return self._media

    @property
    def json(self):
        return json.dumps(self.raw_dump)

    @property
    def host(self):
        url_info = urlparse(self.url)
        return url_info.netloc

    @property
    def thumbnail_url(self):
        return self.dump.get('QUVI_%s_PROPERTY_THUMBNAIL_URL' % self.dump_type)

    @property
    def title(self):
        _title = self.dump.get('QUVI_%s_PROPERTY_TITLE' % self.dump_type)
        _title = urllib.unquote(_title)
        if not _title:
            _title = self.url
        return _title

    @property
    def identifier(self):
        return self.dump.get('QUVI_%s_PROPERTY_ID' % self.dump_type)

    @property
    def duration(self):
        return self._media.get('QUVI_MEDIA_PROPERTY_DURATION_MS')

    @property
    def playlist(self):
        if self.dump_type != 'PLAYLIST':
            return []
        prefix = 'QUVI_PLAYLIST_MEDIA_PROPERTY_'
        return [
            {
                'title': urllib.unquote(item[prefix + 'TITLE']),
                'url': item[prefix + 'URL'],
                'duration': item[prefix + 'DURATION_MS'],
            } for item in self._playlist['media']
        ]


class QuviError(RuntimeError):
    pass


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
