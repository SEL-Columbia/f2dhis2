import json
from django import forms
from django.db.utils import IntegrityError
from django.forms.models import ModelForm
from django.utils.translation import ugettext as _

from main.models import DataSet, DataElement, FormhubService, OrganizationUnit, DataValueSet
from main.utils import load_from_dhis2, load_form_from_formhub


class DataSetImportForm(forms.Form):
    data_set_url = forms.URLField(verify_exists=False,
        label="DHIS2 DataSet URL", required=True)

    def ds_import(self):
        if self.is_valid():
            summary = {}
            cleaned_url = self.cleaned_data['data_set_url']
            if not cleaned_url.endswith('.json'):
                cleaned_url += '.json'
            status, ds_data = load_from_dhis2(cleaned_url)
            if status == 200:
                data = json.loads(ds_data)
                if not isinstance(data, dict):
                    return False
                # period
                frequency = DataSet.get_frequency(data['periodType'])
                try:
                    ds = DataSet(data_set_id=data['id'],
                        name=data['name'],
                        frequency=frequency,
                        url=cleaned_url.replace('.json', ''))
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
                for orgunit in data['organisationUnits']:
                    org, created = OrganizationUnit.objects.get_or_create(org_unit_id=orgunit['id'],
                        name=orgunit['name'])
                    #org.save()
                    ds.organizations.add(org)
                summary['dataSet'] = ds
                summary['dataElements'] = data['dataElements'].__len__()
                summary['orgUnits'] = data['organisationUnits'].__len__()
            return summary
        else:
            return False


class FormhubImportForm(forms.Form):
    formhub_url = forms.URLField(verify_exists=False,
        label=_(u"Formhub Form URL"), required=True)

    def fh_import(self):
        if self.is_valid():
            cleaned_url = self.cleaned_data['formhub_url']
            if not cleaned_url.endswith('/form.json'):
                cleaned_url += '/form.json'
            form_data = load_form_from_formhub(cleaned_url)
            if isinstance(form_data, dict):
                fhs = FormhubService(url=cleaned_url,
                    id_string=form_data['id_string'],
                    name=form_data['name'], json=json.dumps(form_data))
                fhs.save()
                return fhs
        return False


class DataValueSetForm(ModelForm):
    class Meta:
        model = DataValueSet


class FHDataElementForm(forms.Form):
    DVS_TUPLE = tuple([(dvs.pk, '%s' % dvs) for dvs in DataValueSet.objects.all()])
    DVS_SELECT_CHOICES = (('', ' ------ '),) + DVS_TUPLE
    DE_TUPLE = tuple([(de.pk, '%s' % de) for de in DataElement.objects.all()])
    DE_CHOICES = (('', ' ------ '),) + DE_TUPLE

    dvs = forms.ChoiceField(widget=forms.Select, choices=DVS_SELECT_CHOICES)
    data_elements = forms.ChoiceField(widget=forms.Select, choices=DE_CHOICES)
    fh_fields = forms.ChoiceField(widget=forms.Select)

    def set_data_elements_choices(self, dvs):
        self.fields['data_elements'].choices = (('', ' ------ '),)\
                    + tuple([(de.pk, '%s' % de)
                        for de in DataElement.objects.filter(data_set=dvs)])

    def set_fh_fields(self, fhs):
        self.fields['fh_fields'].choices = (('', ' ------ '),)\
                                                + fhs.get_form_fields()
