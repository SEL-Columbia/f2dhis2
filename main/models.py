from django.db import models
from django.utils.translation import ugettext as _


class FormhubService(models.Model):

    class Meta:
        app_label = 'main'
        db_table = 'dhis_formhub_servicet'
        verbose_name = _(u"Formhub Service")
        verbose_name_plural = _(u"Formhub Services")

    url = models.URLField(_(u"URL"))
    name = models.CharField(_(u"Name"), max_length=32)
    id_string = models.CharField(_(u"ID"), max_length=32)
    json = models.TextField(_(u"Json"), )
    created_on = models.DateTimeField(_(u"Created on"), auto_now_add=True)
    modified_on = models.DateTimeField(_(u"Modified on"), auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.id_string)


class DataSet(models.Model):

    FREQUENCY_YEARLY = 1
    FREQUENCY_QUARTERLY = 4
    FREQUENCY_MONTHLY = 12
    FREQUENCY_WEEKLY = 52
    FREQUENCY_DAILY = 256

    PERIOD_CHOICES = {'yearly': FREQUENCY_YEARLY,
                      'quarterly': FREQUENCY_QUARTERLY,
                      'monthly': FREQUENCY_MONTHLY,
                      'weekly': FREQUENCY_WEEKLY,
                      'daily': FREQUENCY_DAILY}

    FREQUENCY_CHOICES = (
        (FREQUENCY_DAILY, _(u"Daily")),
        (FREQUENCY_WEEKLY, _(u"Weekly")),
        (FREQUENCY_MONTHLY, _(u"Monthly")),
        (FREQUENCY_QUARTERLY, _(u"Quarterly")),
        (FREQUENCY_YEARLY, _(u"Yearly")),
    )

    class Meta:
        app_label = 'main'
        db_table = 'dhis_data_set'
        verbose_name = _(u"Data Set")
        verbose_name_plural = _(u"Data Sets")

    data_set_id = models.CharField(_(u"ID"), max_length=32, unique=True)
    name = models.CharField(_(u"Name"), max_length=32)
    frequency = models.PositiveIntegerField(choices=FREQUENCY_CHOICES, default=FREQUENCY_MONTHLY)
    created_on = models.DateTimeField(_(u"Created on"), auto_now_add=True)
    modified_on = models.DateTimeField(_(u"Modified on"), auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.data_set_id)

    @classmethod
    def get_frequency(cls, period):
        return cls.PERIOD_CHOICES[period]


class DataValueSet(models.Model):

    class Meta:
        app_label = 'main'
        db_table = 'dhis_data_value_set'
        verbose_name = _(u"Data Value Set")
        verbose_name_plural = _(u"Data Value Sets")

    service = models.ForeignKey(FormhubService, verbose_name=_(u"Formhub Service"))
    org_unit = models.CharField(_(u"Organization Unit"), max_length=32)
    data_set = models.ForeignKey(DataSet, verbose_name=_(u"Data Set"))
    created_on = models.DateTimeField(_(u"Created on"), auto_now_add=True)
    modified_on = models.DateTimeField(_(u"Modified on"), auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.service, self.data_set)


class DataElement(models.Model):

    class Meta:
        app_label = 'main'
        db_table = 'dhis_data_element'
        verbose_name = _(u"Data Element")
        verbose_name_plural = _(u"Data Elements")
        unique_together = ('data_set', 'data_element_id')

    data_element_id = models.CharField(_(u"ID"), max_length=32)
    name = models.CharField(_(u"Name"), max_length=32)
    data_set = models.ForeignKey(DataSet, verbose_name=_(u"Data Set"))
    created_on = models.DateTimeField(_(u"Created on"), auto_now_add=True)
    modified_on = models.DateTimeField(_(u"Modified on"), auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.data_element_id)


class FormDataElement(models.Model):

    class Meta:
        app_label = 'main'
        db_table = 'dhis_form_data_element'
        verbose_name = _(u"Form Data Element")
        verbose_name_plural = _(u"Form Data Elements")
        unique_together = ('data_value_set', 'data_element')

    data_value_set = models.ForeignKey(DataValueSet, verbose_name=_(u"Data Value Set"))
    data_element = models.ForeignKey(DataElement,verbose_name=_(u"Data Element"))
    form_field = models.CharField(_(u"Form Field"), max_length=32)
    created_on = models.DateTimeField(_(u"Created on"), auto_now_add=True)
    modified_on = models.DateTimeField(_(u"Modified on"), auto_now=True)

    def __unicode__(self):
        return u"%s <=> %s" % (self.data_element, self.form_field)


class DataQueue(models.Model):

    class Meta:
        app_label = 'main'
        db_table = 'dhis_data_queue'
        verbose_name = _(u"Form Data Element")
        verbose_name_plural = _(u"Form Data Elements")

    processed = models.BooleanField(_(u"Processed"), default=False)
    processed_on = models.DateTimeField(_(u"Processed on"), null=True)
    data_id = models.CharField(_(u"Formhub Id"), max_length=32)
    service = models.ForeignKey(FormhubService, verbose_name=_(u"Formhub Service"))
    created_on = models.DateTimeField(_(u"Created on"), auto_now_add=True)
    modified_on = models.DateTimeField(_(u"Modified on"), auto_now=True)

    def __unicode__(self):
        return u"%s - %s" % (self.service, self.data_id)