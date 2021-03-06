from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'f2dhis2.views.home', name='home'),
    # url(r'^f2dhis2/', include('f2dhis2.foo.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),

    url(r'^$', 'main.views.main', name='home'),
    url(r'^(?P<id_string>[^/]+)/post/(?P<uuid>[^/]+)$',
        'main.views.initiate_formhub_request', name='home'),
    url(r'^dataset-import$',
        'main.views.dataset_import', name='dataset-import'),
    url(r'^datasets$',
    'main.views.show_datasets', name='datasets'),
    url(r'^fh-import$',
        'main.views.formhub_import', name='fh-import'),
    url(r'^fh-forms$',
        'main.views.show_formhub_forms', name='fh-forms'),
    url(r'^process-dqueue$',
        'main.views.process_dataqueue', name='process-queue'),
    url(r'^create-dvs',
        'main.views.create_datavalueset', name='create-dvs'),
    url(r'^match-elements',
        'main.views.match_datavalueset_to_data_elements', name='match-de'),
    url(r'^dvs-elements-form/(?P<dvs_id>[^/]+)$',
        'main.views.get_matchdvsform',
        name='match-de-form'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
