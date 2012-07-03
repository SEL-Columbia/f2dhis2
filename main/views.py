from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from django.utils.translation import ugettext as _
from main.forms import DataSetImportForm, FormhubImportForm

from main.models import FormhubService, DataQueue
from main.utils import process_data_queue


def main(request):
    context = RequestContext(request)
    return render_to_response("index.html", context_instance=context)


def initiate_formhub_request(request, id_string, uuid):
    context = RequestContext(request)
    try:
        fs = FormhubService.objects.get(id_string=id_string)
    except FormhubService.DoesNotExist:
        context.contents = _(u"Unknown Service")
        context.status = False
    else:
        dq, created = DataQueue.objects.get_or_create(service=fs, data_id=uuid)
        dq.processed = False
        dq.save()
        context.status = context.status = True
        context.contents = _(u"OK")
    response = {"status": context.status, "contents": context.contents}
    if 'callback' in request.GET and request.GET.get('callback') != '':
        callback = request.GET.get('callback')
        return HttpResponse("%s(%s)" % (callback, simplejson.dumps(response)),
                                                mimetype='application/json')
    return HttpResponse(simplejson.dumps(response),
                            mimetype='application/json')


def dataset_import(request):
    context = RequestContext(request)
    context.form = DataSetImportForm()
    if request.method == 'POST':
        form = DataSetImportForm(request.POST)
        context.rs = form.ds_import()
        if context.rs is False:
            context.failed = True
    return render_to_response("dataset-import.html", context_instance=context)


def formhub_import(request):
    context = RequestContext(request)
    context.form = FormhubImportForm()
    if request.method == 'POST':
        form = FormhubImportForm(request.POST)
        try:
            fhs = form.fh_import()
        except IntegrityError, e:
            context.message = _(u"Form has already been uploaded.")
        else:
            if fhs:
                context.fhservice = fhs
            else:
                context.message = _(u"Failed to import from formhub.")
    return  render_to_response("formhub-import.html", context_instance=context)


def process_dataqueue(request):
    context = RequestContext(request)
    context.processed = process_data_queue()
    return render_to_response("process-queue.html", context_instance=context)
