from django.http.response import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
import data_checker
from dao.nodes import Nodes
import json


# Create your views here.
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
# GET /nodes
# POST /nodes
def node_creation(request):
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
# POST /expertmind_service/create_new_node/
# Accept application/json and the following keys:
#   nodeDisplay
#   nodeDescription
def create_new_node(data):
    # if request.method == 'POST':
    #     print request
        try:
            # data = JSONParser().parse(request)
            data_checker.check_create_new_node(data)
        except Exception, e:
            error = dict(success="false", data={}, error_message=str(e))
            return JSONResponse(error)

        created_node_key = Nodes().create(data["nodeDisplay"], data["nodeDescription"], data["nodeTags"], [],
                              [], [], 1)
        if created_node_key:  # succeeded
            print 'create node: key=', created_node_key
            map_nodes = Nodes().retrieveAll()
            create_node_response = {
                "success": "true",
                "data": map_nodes
            }
        else:
            create_node_response = {
                "success": "false",
                "data": {},
                "error_message": "Orchestrate service temporarily unavailable."
            }
        return JSONResponse(create_node_response)
    # else:  # only allow POST
    #     error = dict(success="false", data={}, error_message="Only POST allowed for node creation.")
    #     return JSONResponse(error)


@csrf_exempt
# POST /expertmind_service/add_child_node/
# Accept application/json and the following keys:
#   nodeDisplay
#   nodeDescription
#   nodeParents [ {"_id" : "..." } ]
#   userId
def add_child_node(data):
    # if request.method == 'POST':
        try:
            # data = JSONParser().parse(request)
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
                    map_nodes = Nodes().retrieveAll()
                    add_child_resp = {
                        "success": "true",
                        "data": map_nodes
                    }
                else:
                    raise ValueError("Update parent node failed during adding a child node.")
            else:
                raise ValueError("Add child node failed.")
            return JSONResponse(add_child_resp)
        except Exception, e:
            print e
            error = dict(success="false", data={}, error_message=str(e))
            return JSONResponse(error)
    # else:  # only allow POST
    #     error = dict(success="false", data={}, error_message="Only POST allowed for adding a child node.")
    #     return JSONResponse(error)


@csrf_exempt
# GET /expertmind_service/get_node_by_id/[node_id]
def get_node_by_id(request, node_id):
    if request.method == 'GET':
        try:
            if node_id == '':
                error = dict(success="false", data={}, error_message="No ID was given when getting node by ID.")
                return JSONResponse(error)

            node_got = Nodes().retrieveById(node_id)

            if 'code' in node_got and node_got['code'] == 'items_not_found': # not found in database
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
# GET /expertmind_service/get_descendant_nodes/[node_id]
def get_descendant_nodes(request, node_id):
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
# GET /expertmind_service/get_child_nodes/[node_id]
def get_child_nodes(request, node_id):
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
# GET /expertmind_service/get_mindmap/
def get_mindmap(request):
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
# /api/votes/
def node_votes(request):
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

            if vote_type == '1': # upvote
                node_after_vote = Nodes().upvoteNode(node_id, user_id, node_comment)
            elif vote_type == '-1': # downvote
                node_after_vote = Nodes().downvoteNode(node_id, user_id, node_comment)

            # node_after_vote = Nodes().retrieveById(node_id)
            success = {
                "success": "true",
                "data": node_after_vote
            }
            return JSONResponse(success)
        except Exception, e:
            print 'POST exception ' + str(e)
            error = dict(success="false", data={}, error_message=str(e))
            return JSONResponse(error)