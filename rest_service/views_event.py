from django.http.response import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
import data_checker
from views import JSONResponse

__author__ = 'hansmong'


@csrf_exempt
def events(request):
    """
    GET /api/events
    POST /api/events
    :param request:
    :return:
    """
    if request.method == 'GET':
        print 'GET'
    elif request.method == 'POST':
        print 'POST'


def get_event_by_id(request, event_id):
    """
    GET /api/events/{event_id}
    :param request:
    :param event_id:
    :return:
    """
    print 'get event by id'


def search_events(request, user_id, node_id):
    """
    GET /api/events?user_id={user_id}&node_id={node_id}
    :param request:
    :param user_id:
    :param node_id:
    :return:
    """
    print 'search event by parameters'
