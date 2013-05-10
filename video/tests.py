"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

from video.utils import get_video_info


class SmokeTest(TestCase):
    def setUp(self):
        self.browser = Client()

    def test_home(self):
        response = self.browser.get('/')
        self.assertEqual(response.status_code, 200)


class TestQuvi(TestCase):

    def test_video_info(self):
        video_url = "https://www.youtube.com/watch?v=Dv9QzbzUZ4M"
        info = get_video_info(video_url)
        self.assertTrue('pageurl' in info)
        self.assertEqual(info['pageurl'], video_url)
        self.assertEqual(info['responsecode'], 200)
