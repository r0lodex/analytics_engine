from django.conf.urls import patterns, include, url
from rest_framework import routers

from api.views import *

router = routers.DefaultRouter()

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^event/(?P<external_id>\w+)/$', store_events, name='store_event'),

    url(r'^query/count/(?P<external_id>\w+)/$', count_queries, name='count_query'),
    url(r'^query/raw_data/(?P<external_id>\w+)/$', raw_queries, name='raw_query'),

)