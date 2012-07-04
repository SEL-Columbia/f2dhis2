from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from main import views
from main.models import DataSet


class Main(TestCase):
    def setUp(self):
        self.username = 'bob'
        self.password = 'bob'
        self.client = Client()
        self.base_url = 'http://testserver'
        self.ds_url = u'http://apps.dhis2.org/demo/api/dataSets/pBOMPrpg1QX'

    def _create_user(self, username, password):
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.save()
        return user

    def _login(self, username, password):
        client = Client()
        assert client.login(username=username, password=password)
        return client


    def test_index_page(self):
        response = self.client.get(reverse(views.main))
        self.assertEqual(response.status_code, 200)

    def test_import_dataset(self):
        ds_import_url = reverse(views.dataset_import)
        response = self.client.get(ds_import_url)
        # need to login first, should redirect
        self.assertEqual(response.status_code, 302)
        self.user = self._create_user(self.username, self.password)
        self.client = self._login(self.username, self.password)
        # should be successful this time
        response = self.client.get(ds_import_url)
        self.assertEqual(response.status_code, 200)
        # check saved Dataset
        count = DataSet.objects.count()
        self.assertEqual(count, 0)
        post_data = {'data_set_url': self.ds_url}
        response = self.client.post(ds_import_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DataSet.objects.count(), count + 1)