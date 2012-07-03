import base64
from datetime import datetime
import urllib
import httplib2
import os.path

from django.conf import settings
from django.utils import simplejson
from django.template.base import Template
from django.template.context import Context

from main.models import DataValueSet, DataSet, DataQueue


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
        # period = self.data['period']
        strdate = datetime.strptime(self.data['period'], '%Y-%m-%d')
        if self.dataValueSet.data_set.frequency == DataSet.FREQUENCY_YEARLY:
            period = strdate.strftime("%Y")
        elif self.dataValueSet.data_set.frequency == DataSet.FREQUENCY_MONTHLY:
            period = strdate.strftime("%Y%m")
        elif  self.dataValueSet.data_set.frequency == DataSet.FREQUENCY_WEEKLY:
            period =  "%s%s" % (strdate.strftime("%Y"),
                                strdate.isocalendar()[1])
        elif self.dataValueSet.data_set.frequency == DataSet.FREQUENCY_DAILY:
            period = strdate.strftime("%Y%m%d")
        else:
            period = strdate.strftime("%Y%m%d")
        return period

    def get_organization_unit(self):
        return self.data['location']

    def get_complete_date(self):
        period = self.data['period']
        return period

    def load_dict(self):
        rs = {
            'dataSet': self.dataValueSet.data_set.data_set_id,
            'orgUnit': self.get_organization_unit()
        }
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
    params = ''
    if id is not None:
        params = urllib.urlencode({'query': '{"_uuid": "%s"}' % id})
    data_api_path = dataValueSet.service.url + u"/api?" + params
    http = httplib2.Http()
    req, content = http.request(data_api_path, 'GET')
    if req.status == 200:
        try:
            return simplejson.loads(content)
        except ValueError, e:
            # TODO: Handle it gracefully
            raise e
    return None


def send_to_dhis2(xml):
    auth = base64.encodestring( settings.DHIS2_USERNAME + ':' + settings.DHIS2_PASSWORD )
    headers = {"Content-Type": "application/xml", 'Authorization' : 'Basic ' + auth}
    http = httplib2.Http()
    http.add_credentials(settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
    resp, content = http.request(settings.DHIS2_DATA_VALUE_SET_URL, 'POST',
        body=xml,
        headers=headers)
    return resp.status, content


def load_from_dhis2(url):
    """
        returns content loaded by given dhis2 url
    """
    auth = base64.encodestring( settings.DHIS2_USERNAME + ':' + settings.DHIS2_PASSWORD )
    headers = {'Authorization' : 'Basic ' + auth}
    http = httplib2.Http()
    http.add_credentials(settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
    resp, content = http.request(url, headers=headers)
    return resp.status, content


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


def process_data_queue():
    """
    Process all queued data
    returns number of processed records
    """
    processed = 0
    for dq in DataQueue.objects.filter(processed=False):
        success = False
        for dvs in DataValueSet.objects.filter(service=dq.service):
            try:
                data = get_data_from_formub(dvs, dq.data_id)
            except Exception, e:
                pass
            else:
                for record in data:
                    xml = get_data_value_set_xml(dvs, record)
                    status, response = send_to_dhis2(xml)
                    success = True
                    print xml, response
        if success:
            dq.processed = True
            dq.processed_on = datetime.now()
            dq.save()
            processed += 1
    return processed


def load_form_from_formhub(url):
    ENDS_WITH = u'form.json'
    if not url.endswith(ENDS_WITH):
        url = u'/'.join([url.strip('/'), ENDS_WITH])
    http = httplib2.Http()
    req, content = http.request(url, 'GET')
    if req.status == 200:
        try:
            return simplejson.loads(content)
        except ValueError, e:
            # TODO: Handle it gracefully
            raise e
    return None
