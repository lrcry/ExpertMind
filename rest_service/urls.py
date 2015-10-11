__author__ = 'hansmong'

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create_new_node/$', views.create_new_node, name='create_new_node'),
    url(r'^add_child_node/$', views.add_child_node, name='add_child_node'),
    url(r'^nodes/(?P<node_id>.+)/$', views.get_node_by_id, name='get_node_by_id'), # get node by its ID
    url(r'^nodes/(?P<node_id>.+)/descendant/$', views.get_descendant_nodes, name='get_descendant_nodes'), # get descendant
    url(r'^nodes/(?P<node_id>.+)/children/$', views.get_child_nodes, name='get_child_nodes'), # get children
    url(r'^nodes/$', views.get_mindmap, name='get_mindmap'), # get all nodes

    url(r'^votes/$', views.node_votes, name='node_votes'), # POST node votes
]