"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client


class SmokeTest(TestCase):
    def setUp(self):
        self.browser = Client()

    def test_home(self):
        response = self.browser.get('/')
        self.assertEqual(response.status_code, 200)
