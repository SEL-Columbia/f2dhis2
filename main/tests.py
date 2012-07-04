from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from main import views


class Main(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_url = 'http://testserver'

    def test_index_page(self):
        response = self.client.get(reverse(views.main))
        self.assertEqual(response.status_code, 200)