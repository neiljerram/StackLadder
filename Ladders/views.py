from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.db.models import Count

from .models import Event

def index(request):
    return HttpResponse("Hello World! There will eventually be a ladder diagram here!")

def source(request, source_id):
    event_list = Event.objects.filter(source=source_id).order_by('-time_stamp').reverse()
    template = loader.get_template('Ladders/source-wsd.html')
    context = RequestContext(request, {'event_list' : event_list })
    return HttpResponse(template.render(context))

def dest(request, dest_id):
    event_list = Event.objects.filter(dest=dest_id).order_by('-time_stamp').reverse()
    template = loader.get_template('Ladders/dest-wsd.html')
    context = RequestContext(request, {'event_list' : event_list })
    return HttpResponse(template.render(context))

def allevents(request, endpoint_id):
    event_list = Event.objects.filter(dest=endpoint_id) | Event.objects.filter(source=endpoint_id)
    event_list = event_list.order_by('-time_stamp').reverse()
    template = loader.get_template('Ladders/all-wsd.html')
    context = RequestContext(request, {'event_list' : event_list })
    return HttpResponse(template.render(context))

def nt1(request, endpoint_id):
    event_list = Event.objects.filter(dest=endpoint_id) | Event.objects.filter(source=endpoint_id)
    event_list = event_list.order_by('-time_stamp').reverse()
    event_list = list(event_list)

    #Get a list of unique destinations
    dest_list = set([])
    for event in event_list:
        if event.dest != endpoint_id:
            dest_list.add(event.dest)
    dest_count = len(dest_list)

    html_header = """<!DOCTYPE HTML>
<html>
  <head>
    <style>
      body {
        margin: 0px;
        padding: 0px;
      }
    </style>
  </head>
  <body>"""

    html_body = """"""

    html_footer = """    
  </body>
</html>"""
 
    line_x = 400 
    x_line_sep = 360
    event_y = 75
    event_y_sep = 50
 
    canvas_width = x_line_sep*(dest_count+3)
    canvas_height = 50*(len(event_list)+1)

    html_body += """<canvas id="myCanvas" width=%s height=%s></canvas>
    <script>
      var canvas = document.getElementById('myCanvas');
      var ladder = canvas.getContext('2d');""" % (canvas_width, canvas_height)

    # Draw headings and lines for each source/destination
    html_body += """
      ladder.font = '24pt Calibri';
      ladder.textAlign = 'center';
      ladder.fillText('%(endpoint_id)s', %(line_x)s, 25);""" % { "endpoint_id" : endpoint_id,
                                                                 "line_x" : line_x }

    html_body += """
      ladder.lineWidth = 15;
      ladder.strokeStyle = '#ff0000';

      ladder.beginPath();
      ladder.moveTo(%(line_x)s, 30);
      ladder.lineTo(%(line_x)s, %(canvas_height)s);
      ladder.stroke();""" % { "line_x" : line_x, "canvas_height" : canvas_height}

    x_pos_lookup = { endpoint_id : line_x }


    for dest in dest_list:
        line_x += x_line_sep
	html_body += """
      ladder.fillText('%(dest_name)s', %(line_x)s, 25);

      ladder.beginPath();
      ladder.moveTo(%(line_x)s, 30);
      ladder.lineTo(%(line_x)s, %(canvas_height)s);
      ladder.stroke();""" % { "line_x" : str(line_x),
                              "canvas_height" : str(canvas_height),
                              "dest_name" : str(dest)}

    x_pos_lookup[dest] = line_x

    html_body += """
      ladder.lineWidth = 5;
      ladder.strokeStyle = '#000000';

"""


    for event in event_list:
        # First output the time-stamp:
        event_body = """

      ladder.font = '16pt Calibri';
      ladder.textAlign = 'left';
      ladder.textBaseline = 'middle'; 
      ladder.fillText('%(time_stamp)s', 10, %(event_y)s)"""

        # Draw a line:
        event_body += """
      ladder.beginPath();
      ladder.moveTo(%(source_x)s, %(event_y)s);
      ladder.lineTo(%(dest_x)s, %(event_y)s);
      ladder.stroke();
      """

        # Setup variables, then draw an arrow:
        source_x = x_pos_lookup[event.source]
        dest_x = x_pos_lookup[event.dest]
        arrow_y_plus = event_y + 20
        arrow_y_minus = event_y - 20
        if source_x > dest_x:
            arrow_x = dest_x + 20
        else:
            arrow_x = dest_x - 20

        event_body += """
      ladder.beginPath();
      ladder.moveTo(%(dest_x)s, %(event_y)s);
      ladder.lineTo(%(arrow_x)s, %(arrow_y_plus)s);
      ladder.lineTo(%(arrow_x)s, %(arrow_y_minux)s);
      ladder.fill();
 
      """
        
        # Add the event summary:
        label_x = ( source_x + dest_x ) / 2
        
        event_body += """
      ladder.font = '14pt Courier';
      ladder.textAlign = 'center';
      ladder.textBaseline = 'bottom'; 
      ladder.fillText('%(summary)s', %(label_x)s, %(event_y)s);
      """
 
        event_body = event_body % { "time_stamp" : event.time_stamp,
                                    "event_y" : event_y,
                                    "source_x": source_x,
                                    "dest_x": dest_x,
                                    "arrow_x" : arrow_x,
                                    "arrow_y_plus" : arrow_y_plus,
                                    "arrow_y_minux" : arrow_y_minus,
                                    "summary" : event.summary[0:30],
                                    "label_x" : label_x,
 }

        html_body += event_body
        event_y += event_y_sep


    html_body += """
      </script>"""

    html_source = html_header+html_body+html_footer
    return HttpResponse(html_source)

def canvas():
    pass


# Create your views here.
