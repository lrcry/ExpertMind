from django.http.response import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
import data_checker
from views import JSONResponse
from dao.events import Events

__author__ = 'hansmong'


@csrf_exempt
def events(request):
    """
    GET /api/events[?user_id={user_id}&node_id={node_id}&status=[status]]
    POST /api/events
    :param request:
    :return:
    """
    try:
        if request.method == 'GET':
            events_list = Events.retrieve_all()
            if events_list is not []:  # not empty list
                node_id = request.GET.get('node_id', '')
                user_id = request.GET.get('user_id', '')

                events_search_list = []
                if node_id is not '' and user_id is not '':  # both node id and user id
                    for event in events_list:
                        if event['node_id'] == node_id and event['user_id'] == user_id:
                            events_search_list.append(event)

                    resp = {
                        'success': 'true',
                        'data': events_search_list
                    }

                elif node_id is not '':  # only by node id
                    for event in events_list:
                        if event['node_id'] == node_id:
                            events_search_list.append(event)

                    resp = {
                        'success': 'true',
                        'data': events_search_list
                    }

                elif user_id is not '':  # only by user id
                    for event in events_list:
                        if event['user_id'] == user_id:
                            events_search_list.append(event)

                    resp = {
                        'success': 'true',
                        'data': events_search_list
                    }

                else:  # all
                    resp = {
                        'success': 'true',
                        'data': events_list
                    }

            else:
                resp = {
                    'success': 'true',
                    'data': events_list
                }

        elif request.method == 'POST':
            data = JSONParser().parse(request)
            data_checker.check_create_event(data)

            created_event_key = Events.create(data)

            if created_event_key:
                print 'create event successful'
                resp = {
                    'success': 'true',
                    'data': created_event_key
                }
            else:
                raise RuntimeError('Orchestrate service temporarily unavailable')
        else:
            raise NotImplementedError('Only GET, POST methods are allowed')

        return JSONResponse(resp)
    except Exception, e:
        err = {
            'success': 'false',
            'data': {},
            'err_message': str(e)
        }

        return JSONResponse(err)


def event_by_id(request, event_id):
    """
    GET /api/events/{event_id}
    PUT /api/events/{event_id}
    :param request:
    :param event_id:
    :return:
    """
    if request.method == 'GET':
        print 'get event by id'
        try:
            if event_id == '':
                raise ValueError('No ID is given while trying to get event by ID')

            event_get = Events.retrieve_by_id(event_id)
            if 'code' in event_get and event_get['code'] == 'items_not_found':
                raise ValueError('No event found with given id=' + event_id)

            event_response = {
                'success': 'true',
                'data': event_get
            }
            return JSONResponse(event_response)
        except Exception, e:
            err = {
                'success': 'false',
                'data': {},
                'err_message': str(e)
            }
            return JSONResponse(err)

    elif request.method == 'PUT':
        print 'put update by event id'
        # TODO PUT update by event id (mainly for status)

    else:
        err = {
            "success": "false",
            "err_message": "Only GET method is allowed",
            "data": {}
        }
