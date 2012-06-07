import json
from django import forms
from django.db.utils import IntegrityError
from django.utils.translation import ugettext as _

from main.models import DataSet, DataElement
from main.utils import load_from_dhis2


class DataSetImportForm(forms.Form):
    data_set_url = forms.URLField(verify_exists=False,
        label="DHIS2 DataSet URL", required=True)

    def ds_import(self):
        if self.is_valid():
            summary = {}
            cleaned_url = self.cleaned_data['data_set_url']
            if cleaned_url[-4:] != '.json':
                cleaned_url += '.json'
            status, ds_data = load_from_dhis2(cleaned_url)
            if status == 200:
                data = json.loads(ds_data)
                # period
                frequency = DataSet.get_frequency(data['periodType'])
                try:
                    ds = DataSet(data_set_id=data['id'],
                        name=data['name'],
                        frequency=frequency)
                    ds.save()
                except IntegrityError, e:
                    return {
                        'ds_status':
                            _(u"%(dataset)s has already been added." %\
                              {'dataset': data['name']})}
                for de in data['dataElements']:
                    element = DataElement(data_element_id=de['id'],
                        name=de['name'],
                        data_set=ds)
                    element.save()
                summary['dataSet'] = ds
                summary['dataElements'] = data['dataElements'].__len__()
            return summary
        else:
            return False