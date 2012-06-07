from django import forms


class DataSetImportForm(forms.Form):
    data_set_url = forms.URLField(verify_exists=False,
                                    label="DHIS2 DataSet URL", required=True)

    def ds_import(self):
        if self.is_valid():
            return True
        else:
            return False