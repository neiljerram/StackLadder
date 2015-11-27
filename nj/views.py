from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.db.models import Count

from . import models

# Create your views here.

def index(request):
    rec_list = models.Record2.objects.order_by('time_stamp')
    template = loader.get_template('nj/template.html')
    context = RequestContext(request, {'rec_list' : rec_list })
    return HttpResponse(template.render(context))

def columns(request):
    columns = set()
    for r in models.Record2.objects.all():
        columns.add(r.src_name)
        columns.add(r.dst_name)

    template = loader.get_template('nj/column_names.html')
    context = RequestContext(request, {'columns' : columns })
    return HttpResponse(template.render(context))

def endpoints(request):
    endpoints = set()
    as_client = {}
    as_server = {}
    for r in models.Record2.objects.all():

        response = False
        if r.summary.startswith('HTTP'):
            # Record indicates an HTTP response.
            response = True

        endpoint = (r.src_ip, r.src_name)
        endpoints.add(endpoint)
        if response:
            as_server[endpoint] = True
        else:
            as_client[endpoint] = True

        endpoint = (r.dst_ip, r.dst_name)
        endpoints.add(endpoint)
        if response:
            as_client[endpoint] = True
        else:
            as_server[endpoint] = True


    html = """
<div class=wsd wsd_style="magazine">
<h2>Endpoints</h2>
<table border=1>
<tr><th>IP address</th><th>Service</th><th>Client?</th><th>Server?</th></tr>
"""

    for e in endpoints:
        (ip, name) = e
        html += ('<tr><td>' + ip +
                 '</td><td>' + name +
                 '</td><td>' + str(as_client.get(e, '')) +
                 '</td><td>' + str(as_server.get(e, '')) +
                 '</td><td><a href="endpoint/' + ip + '/' + name + '">Details</a>' +
                 '</td></tr>\n')

    html += """
</table>
"""

    return HttpResponse(html)

def endpoint(request, ip, name):
    rec_list = [x for x in models.Record2.objects.order_by('time_stamp') if
                (((x.src_ip == ip) and (x.src_name == name)) or
                 ((x.dst_ip == ip) and (x.dst_name == name)))]

    rec_list = rec_list[-200:]

    html = """
    <script type="text/javascript">
        function mkvis(id) {
           var e = document.getElementById(id);
           if(e.style.display == 'block')
              e.style.display = 'none';
           else
              e.style.display = 'block';
        }
    </script><div class=wsd wsd_style="magazine">
"""

    html += '<h2>Events for ' + ip + ' ' + name + '</h2>\n'

    html += '<table>\n'

    for r in rec_list:
        html += '<tr><td style="font-size:70%;">' + str(r.time_stamp) + '</td><td>'
        html += '<a href="javascript:mkvis(\'' + str(r.id) + '\')">' + r.summary + '</a>\n'
        #html += '<a href="#' + str(r.id) + '" onclick="mkvis(\'' + str(r.id) + '\')">' + r.summary + '</a>\n'
        html += ('<div id="' + str(r.id) + '" style="display: none;"><pre>\n' +
                 r.detail + '</pre></div>\n')
        html += '</td></tr>'

    return HttpResponse(html)
