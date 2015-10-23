__author__ = 'hansmong'

from django.conf.urls import url
from . import views
from . import views_event

"""
Defines the URI of accessing REST services
"""
urlpatterns = [

    url(r'^nodes/(?P<node_id>.+)$', views.get_node_by_id, name='get_node_by_id'),  # get node by its ID
    url(r'^nodes/(?P<node_id>.+)/descendant$', views.get_descendant_nodes, name='get_descendant_nodes'),  # get descendant
    url(r'^nodes/(?P<node_id>.+)/children$', views.get_child_nodes, name='get_child_nodes'),  # get children
    url(r'^nodes$', views.node_creation, name='node_creation'),  # GET/POST /api/nodes
    url(r'^votes$', views.node_votes, name='node_votes'),  # POST node votes
    url(r'^events$', views_event.events, name='events'),  # POST node events
    url(r'^events/(?P<event_id>.+)$', views_event.event_by_id, name='event'),  # GET/PUT event by its ID
]