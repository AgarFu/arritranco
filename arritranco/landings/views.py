from models import Landing
from django.shortcuts import render_to_response

def nagios_landings(request):
    '''
        Nagios landing checks config file.
    '''
    template = 'landings/nagios.cfg'
    context = {}
    context['landings'] = Landing.objects.filter(enable = True).order_by('type')
    if 'file' in request.GET:
        response = render_to_response(template, context, mimetype="text/plain")
        response['Content-Disposition'] = 'attachment; filename=%s' % request.GET['file'] 
    else:
        response = render_to_response(template, context, mimetype="text/plain")
    return response
