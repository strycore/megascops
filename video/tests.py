"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client


class SmokeTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
