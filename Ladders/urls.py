from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^allevents/(?P<endpoint_id>[^/]+)/$', views.allevents, name='AllEvents'),
    url(r'^source/(?P<source_id>[^/]+)/$', views.source, name='Source'),
    url(r'^dest/(?P<dest_id>[^/]+)/$', views.dest, name='Dest'),
    url(r'^nt1/(?P<endpoint_id>[^/]+)/$', views.nt1, name='NT1 Source'),
]

