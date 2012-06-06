from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from django.utils.translation import ugettext as _

from main.models import FormhubService, DataQueue


def initiate_formhub_request(request, id_string, id):
    context = RequestContext(request)
    try:
        fs = FormhubService.objects.get(id_string=id_string)
    except FormhubService.DoesNotExist:
        context.contents = _(u"Unknown Service")
        context.status = False
    else:
        dq, created = DataQueue.objects.get_or_create(service=fs, data_id=id)
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
