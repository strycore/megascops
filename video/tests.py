"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

from video.utils import get_streams


class SmokeTest(TestCase):
    def setUp(self):
        self.browser = Client()

    def test_home(self):
        response = self.browser.get('/')
        self.assertEqual(response.status_code, 200)


class TestQuvi(TestCase):

    def test_video_info(self):
        video_url = "https://www.youtube.com/watch?v=Dv9QzbzUZ4M"
        streams = get_streams(video_url)
        self.assertTrue('QUVI_MEDIA_STREAM_PROPERTY_CONTAINER' in streams[0])
