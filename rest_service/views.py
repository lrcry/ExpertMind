from django.http.response import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
import data_checker
from dao.nodes import Nodes
import json
import requests

"""
Nodes services defined here
"""


# Create your views here.
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def node_creation(request):
    """
    GET /api/nodes to get all the nodes from the database
    POST /api/nodes to create a new node to the database
    :param request: HTTP request of service
    :return: JSON response which contains the result of get/create node
    """

    if request.method == 'GET':
        node_response = get_mindmap(request)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        if 'nodeParents' not in data:
            node_response = create_new_node(data)
        else:
            node_response = add_child_node(data)
    return node_response


@csrf_exempt
def get_node_by_id(request, node_id):
    """ Get a node by its ID
    GET /api/nodes/{node_id}
    :param request:
    :param node_id:
    :return:
    """
    if request.method == 'GET':
        try:
            if node_id == '':
                error = dict(success="false", data={}, error_message="No ID was given when getting node by ID.")
                return JSONResponse(error)

            node_got = Nodes().retrieveById(node_id)

            if 'code' in node_got and node_got['code'] == 'items_not_found':  # not found in database
                no_node_response = {
                    "success": "true",
                    "data": "No node found with _id = %s" % node_id
                }
                return JSONResponse(no_node_response)

            get_node_by_id_response = {
                "success": "true",
                "data": node_got
            }
            return JSONResponse(get_node_by_id_response)
        except Exception, e:
            error = dict(success="false", data={}, error_message=str(e))
            return JSONResponse(error)
    else:  # only allow GET
        error = dict(success="false", data={}, error_message="Only GET allowed for getting a node by ID.")
        return JSONResponse(error)


@csrf_exempt
def get_descendant_nodes(request, node_id):
    """ Get all descendant nodes of a node
    GET /api/nodes/{node_id}/descendant
    :param request:
    :param node_id:
    :return:
    """
    if request.method == 'GET':
        try:
            if node_id == '':
                error = dict(success="false", data={}, error_message="No ID was given when getting descendant nodes of"
                                                                     "a node by its ID.")
                return JSONResponse(error)

            descendant_nodes_list = Nodes().retrieveDescendent(node_id)
            get_descendant_nodes_response = {
                "success": "true",
                "data": descendant_nodes_list
            }
            return JSONResponse(get_descendant_nodes_response)
        except Exception, e:
            error = dict(success="false", data={}, error_message=str(e))
            return JSONResponse(error)
    else:  # only allow GET
        error = dict(success="false", data={}, error_message="Only GET allowed for getting descendant nodes of"
                                                             "a node by its ID.")
        return JSONResponse(error)


@csrf_exempt
def get_child_nodes(request, node_id):
    """ Get all the direct children of a node
    GET /api/nodes/{node_id}/children
    :param request:
    :param node_id:
    :return:
    """
    if request.method == 'GET':
        try:
            if node_id == '':
                error = dict(success="false", data={}, error_message="No ID was given when getting children nodes of"
                                                                     "a node by its ID.")
                return JSONResponse(error)

            children_nodes_list = Nodes().retrieveChild(node_id)
            get_children_nodes_response = {
                "success": "true",
                "data": children_nodes_list
            }
            return JSONResponse(get_children_nodes_response)
        except Exception, e:
            error = dict(success="false", data={}, error_message=str(e))
            return JSONResponse(error)
    else:  # only allow GET
        error = dict(success="false", data={}, error_message="Only GET allowed for getting children nodes of"
                                                             "a node by its ID.")
        return JSONResponse(error)


@csrf_exempt
def get_mindmap(request):
    """
    Service for getting all the nodes
    :param request:
    :return:
    """
    if request.method == 'GET':
        try:
            node_list = Nodes().retrieveAll()
            resp_map = {
                "success": "true",
                "data": node_list
            }
            return JSONResponse(resp_map)
        except Exception, e:
            resp_error = {
                "success": "false",
                "data": {},
                "error_message": str(e)
            }
            return JSONResponse(resp_error)
    else:  # only allow GET
        error = dict(success="false", data={}, error_message="Only GET allowed for getting the mindmap.")
        return JSONResponse(error)


@csrf_exempt
def node_votes(request):
    """ Create a new vote on a node
    POST /api/votes
    :param request:
    :return:
    """
    if request.method == 'GET':
        print 'GET - why do you want to get this again?'
        get_error = {
            "success": "false",
            "data": {},
            "error_message": "GET - why do you want to get this again?"
        }
        return JSONResponse(get_error)
    elif request.method == 'POST':
        try:
            vote_data = JSONParser().parse(request)
            data_checker.check_vote_node(vote_data)

            user_id = vote_data["userId"]
            vote_type = vote_data["type"]
            node_id = vote_data["nodeId"]
            node_comment = vote_data["comment"]
            print node_comment + " as node comment"

            event_url = 'http://localhost:8000/api/events'

            if vote_type == '1': # upvote
                node_after_vote = Nodes().upvoteNode(node_id, user_id, node_comment)
                event = {
                    'user_id': user_id if user_id else 'Anonymous',
                    'node_id': node_id,
                    'operation': data_checker.VOTE_UP
                }
            elif vote_type == '-1': # downvote
                node_after_vote = Nodes().downvoteNode(node_id, user_id, node_comment)
                event = {
                    'user_id': user_id if user_id else 'Anonymous',
                    'node_id': node_id,
                    'operation': data_checker.VOTE_UP
                }
            else:
                raise ValueError('Error when voting: only accept 1 and -1 as valid vote')

            event_response = requests.post(event_url, json.dumps(event))
            if 'success' in event_response.json() and event_response.json()['success'] == 'true':
                success = {
                    "success": "true",
                    "data": node_after_vote
                }
            else:
                raise RuntimeError("Error when creating new event: " + event_response.json()['err_message'])

            return JSONResponse(success)
        except Exception, e:
            print 'POST exception ' + str(e)
            error = dict(success="false", data={}, error_message=str(e))
            return JSONResponse(error)

@csrf_exempt
def create_new_node(data):
    """
    Service support for creating a new node
    :param data:
    :return:
    """
    try:
        data_checker.check_create_new_node(data)
    except Exception, e:
        error = dict(success="false", data={}, error_message=str(e))
        return JSONResponse(error)

    created_node_key = Nodes().create(data["nodeDisplay"], data["nodeDescription"], data["nodeTags"], [],
                          [], [], 1)
    if created_node_key:  # succeeded
        print 'create node: key=', created_node_key
        map_nodes = Nodes().retrieveAll()

        # create an event of creating new nodes for this user
        event_url = 'http://localhost:8000/api/events'
        event = {
            'user_id': data['userId'] if 'userId' in data else 'Anonymous',
            'node_id': created_node_key,
            'operation': data_checker.CREATE_NEW_NODE
        }

        event_response = requests.post(event_url, json.dumps(event))
        if 'success' in event_response.json() and event_response.json()['success'] == 'true':
            create_node_response = {
                "success": "true",
                "data": map_nodes
            }
        else:
            create_node_response = {
                "success": "false",
                "data": {},
                "error_message": "Error when creating new event: " + event_response.json()['err_message']
            }
    else:
        create_node_response = {
            "success": "false",
            "data": {},
            "error_message": "Orchestrate service temporarily unavailable."
        }
    return JSONResponse(create_node_response)


@csrf_exempt
def add_child_node(data):
    """
    Service support of add a child node
    :param data:
    :return:
    """
    try:
        parent_node = data_checker.check_add_child_node(data)

        if 'nodeTags' not in data:
            data["nodeTags"] = []  # not required

        if 'nodeChildren' not in data:
            data["nodeChildren"] = []

        if 'nodeVotes' not in data:
            data["nodeVotes"] = []
        else:
            if 'comment' not in data['nodeVotes']:
                data["nodeVotes"]["comment"] = ""

        print 'something wrong before create node vote comment'
        node_status = 1

        created_child_node_key = Nodes().create(
            data["nodeDisplay"],
            data["nodeDescription"],
            data["nodeTags"],
            data["nodeParents"],
            data["nodeChildren"],
            data["nodeVotes"],
            node_status
        )

        if created_child_node_key:
            print 'add child node: key=', created_child_node_key
            print parent_node['_id'], parent_node['nodeChildren']
            parent_node["nodeChildren"].append({
                "_id": created_child_node_key
            })

            parent_node_update = Nodes().update(parent_node["_id"],
                                                parent_node["nodeDisplay"],
                                                parent_node["nodeDescription"],
                                                parent_node["nodeTags"],
                                                parent_node["nodeParents"],
                                                parent_node["nodeChildren"],
                                                parent_node["nodeVotes"],
                                                parent_node["nodeStatus"],
                                                parent_node["nodeCreateAt"])

            if parent_node_update:
                print "update parent: key=", parent_node_update

                # create an event of adding a child node for this user
                event_url = 'http://localhost:8000/api/events'
                event = {
                    'user_id': data['userId'] if 'userId' in data else 'Anonymous',
                    'node_id': parent_node_update,
                    'operation': data_checker.ADD_CHILD_NODE
                }

                event_response = requests.post(event_url, json.dumps(event))

                if 'success' in event_response.json() and event_response.json()['success'] == 'true':
                    map_nodes = Nodes().retrieveAll()
                    add_child_resp = {
                        "success": "true",
                        "data": map_nodes
                    }
                else:
                    raise RuntimeError('Error adding child node: ' + event_response.json()['err_message'])

            else:
                raise ValueError("Update parent node failed during adding a child node.")
        else:
            raise ValueError("Add child node failed.")
        return JSONResponse(add_child_resp)
    except Exception, e:
        print e
        error = dict(success="false", data={}, error_message=str(e))
        return JSONResponse(error)
