import base64
import httplib
import urllib
from django.conf import settings
import httplib2
import os.path

from urlparse import urlparse
from django.utils import simplejson

from django.template.base import Template
from django.template.context import Context
from main.models import DataValueSet, DataSet


class DataValueSetInterface(object):
    template_name = "datavalueset.xml"
    template = None
    dataValueSet = None
    data = {}
    data_elements = []

    def __init__(self, dataValueSet, data=None):
        self.dataValueSet  = dataValueSet
        self.data = data
        self.load_template()

    def load_template(self):
        filename = os.path.abspath(os.path.join(os.path.dirname(__file__),"templates/%s" % self.template_name))
        f = open(filename)
        self.template = Template(f.read())
        f.close()

    def load_data_elements(self):
        elements = []
        if self.data is not None:
            for fe in self.dataValueSet.formdataelement_set.all():
                if self.data.has_key('%s' % fe.form_field):
                    element = {'id': fe.data_element.data_element_id, 'value': self.data['%s' % fe.form_field]}
                    elements.append(element)
        self.data_elements = elements

    def get_period(self):
        period = self.data['period']
        if self.dataValueSet.data_set.frequency == DataSet.FREQUENCY_YEARLY:
            period = ''.join(period.split('-')[0])
        elif self.dataValueSet.data_set.frequency == DataSet.FREQUENCY_MONTHLY:
            period = ''.join(period.split('-')[:2])
        elif self.dataValueSet.data_set.frequency == DataSet.FREQUENCY_DAILY:
            period = ''.join(period.split('-')[:3])
        else:
            period = ''.join(period.split('-'))
        return period

    def get_complete_date(self):
        period = self.data['period']
        return period

    def load_dict(self):
        rs = {'dataSet': self.dataValueSet.data_set.data_set_id, 'orgUnit': self.dataValueSet.org_unit}
        if self.data is not None and len(self.data):
            self.load_data_elements()
            rs['period'] = self.get_period()
            rs['completeDate'] = self.get_complete_date()
            rs['dataElements'] =  self.data_elements
        return rs

    def render(self):
        return self.template.render(Context(self.load_dict()))


def get_data_value_set_xml(dataValueSet, data=None):
    dvsi = DataValueSetInterface(dataValueSet, data)
    return dvsi.render()


def get_data_from_formub(dataValueSet, id=None):
    url = urlparse(dataValueSet.service.url)
    params = None
    if id is not None:
        params = urllib.urlencode({'query': '{"_id": %s}' % id})
    data_api_path = url.path + u"/api?" + params
    print params
    conn = httplib.HTTPConnection(url.netloc)
    conn.request("GET", data_api_path)
    req = conn.getresponse()
    if req.status == 200:
        data = req.read()
        print data
        try:
            return simplejson.loads(data)
        except ValueError, e:
            req.close()
            raise e
    req.close()
    return None


def send_to_dhis2(xml):
    auth = base64.encodestring( settings.DHIS2_USERNAME + ':' + settings.DHIS2_PASSWORD )
    headers = {"Content-Type": "application/xml", 'Authorization' : 'Basic ' + auth}
    http = httplib2.Http()
    http.add_credentials(settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
    resp, content = http.request(settings.DHIS2_DATA_VALUE_SET_URL, 'POST',
        body=xml,
        headers=headers)
    print resp.status, content


def test_f2dhis():
    dvs = DataValueSet.objects.all()[0]
    try:
        data = get_data_from_formub(dvs, 3)
    except Exception, e:
        print e
    else:
        print data
        for record in data:
            xml = get_data_value_set_xml(dvs, record)
            print xml
            send_to_dhis2(xml)