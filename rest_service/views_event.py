from rest_framework.parsers import JSONParser
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
                status = request.GET.get('status', '')

                if status is not '' and status not in data_checker.VALID_EVENT_STATUS_LIST:
                    raise ValueError('Status ' + status + ' is not valid')

                node_search = node_id is not ''
                user_search = user_id is not ''
                status_search = status is not ''

                events_search_list = []

                if node_search or user_search or status_search:  # has parameters to search
                    if node_search and user_search and status_search:  # search by node, user and status
                        for event in events_list:
                            if event['node_id'] == node_id and event['user_id'] == user_id and event['status'] == status:
                                events_search_list.append(event)

                    elif node_search and user_search:  # search by node and user
                        for event in events_list:
                            if event['node_id'] == node_id and event['user_id'] == user_id:
                                events_search_list.append(event)

                    elif user_search and status_search:  # search by user and status
                        for event in events_list:
                            if event['user_id'] == user_id and event['status'] == status:
                                events_search_list.append(event)

                    elif node_search and status_search:  # search by node and status
                        for event in events_list:
                            if event['node_id'] == node_id and event['status'] == status:
                                events_search_list.append(event)

                    elif user_search:  # search only by user
                        for event in events_list:
                            if event['user_id'] == user_id:
                                events_search_list.append(event)

                    elif node_search:  # search only by node
                        for event in events_list:
                            if event['node_id'] == node_id:
                                events_search_list.append(event)

                    elif status_search:  # search only by status
                        for event in events_list:
                            if event['status'] == status:
                                events_search_list.append(event)

                    resp = {
                        'success': 'true',
                        'data': events_search_list
                    }

                else:  # all without parameters
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
            data_checker.check_event(data, request.method)

            created_event_key = Events.create(data)

            if created_event_key:
                print 'create event successful'
                if 'user_id' not in data:
                    resp = {
                        'success': 'true',
                        'data': created_event_key
                    }
                else:
                    all_events_list = Events.retrieve_all()
                    resp_events = []
                    for event in all_events_list:
                        if event['user_id'] == data['user_id'] and event['status'] == data_checker.EVENT_UNREAD:
                            resp_events.append(event)

                    resp = {
                        'success': 'true',
                        'data': resp_events
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


@csrf_exempt
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
        try:
            data = JSONParser().parse(request)
            data_checker.check_event(data, request.method)

            update_event_key = Events.update(event_id, data)

            if update_event_key:
                print 'create event successful'
                if 'user_id' not in data:
                    resp = {
                        'success': 'true',
                        'data': update_event_key
                    }
                else:
                    all_events_list = Events.retrieve_all()
                    resp_events = []
                    for event in all_events_list:
                        if event['user_id'] == data['user_id'] and event['status'] == data_checker.EVENT_UNREAD:
                            resp_events.append(event)

                    resp = {
                        'success': 'true',
                        'data': resp_events
                    }
            else:
                raise RuntimeError('Orchestrate service temporarily unavailable')

        except Exception, e:
            err = {
                'success': 'false',
                'data': {},
                'err_message': str(e)
            }
            return JSONResponse(err)

        return JSONResponse(resp)
    else:
        err = {
            "success": "false",
            "err_message": "Only GET and PUT method is allowed",
            "data": {}
        }
        return JSONResponse(err)
