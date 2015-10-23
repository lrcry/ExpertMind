from dao.tag import Tag
from dao.nodes import Nodes


__author__ = 'hansmong'


PERMITTED_OPERATION_LIST = ['CREATE_NEW_NODE', 'ADD_CHILD_NODE', 'VOTE_UP', 'VOTE_DOWN']


def check_add_child_node(data):
    """ Check data when adding a new child node
    To be more specific, the following keys will be checked
        nodeDisplay
        nodeDescription
        nodeTags
        nodeParents

    :param data: new child node json data
    :return: the parent node of check for update reason
    """

    # check nodeDisplay
    """

    :rtype :
    """
    if 'nodeDisplay' not in data:
        raise ValueError("No nodeDisplay in given node.")

    # check nodeDescription
    if 'nodeDescription' not in data:
        raise ValueError("No nodeDescription in given node.")

    # check nodeTags
    if 'nodeTags' not in data:
        data["nodeTags"] = []

    # check nodeParents
    if 'nodeParents' not in data or len(data["nodeParents"]) == 0:
        raise ValueError("No nodeParents in given node.")
    else:
        parent = data["nodeParents"][0]
        if '_id' not in parent:
            raise ValueError("Malformed node parent array: lack of parent node id \"_id\"")
        else:
            parent_node = Nodes().retrieveById(parent["_id"])
            if parent_node.status_code == 404:
                raise ValueError(
                    "Parent node information does not exist in database: parent _id=%s" % parent["_id"])
            else:
                return parent_node

# check add child node data end


def check_create_new_node(data):
    """ Check json data performing when create a new (root) node
    This function will check the required keys and values in input json data
    To be more specific, the following keys are checked
        nodeDisplay
        nodeDescription
        nodeTags

    :param data: new node data
    :return: nothing
    """

    # check nodeDisplay
    if 'nodeDisplay' not in data:
        raise ValueError("No nodeDisplay in given node.")

    # check nodeDescription
    if 'nodeDescription' not in data:
        raise ValueError("No nodeDescription in given node.")

    # check nodeTags
    if 'nodeTags' not in data:
        data["nodeTags"] = {}
    else:
        for node_tag in data["nodeTags"]:
            if '_id' not in node_tag:
                raise ValueError("Malformed node tag array: lack of tag id \"_id\"")
            else:
                if Tag.retrieveById(node_tag["_id"]) is None:  # non-existent node tag in database
                    raise ValueError("Node tag does not exist in database: tag _id=%s" % node_tag["_id"])


# check input vote on a node
def check_vote_node(data):
    """ Check votes on a node
    The following keys are to be checked
        userId
        type
        nodeId

    :param data: json data of a vote
    :return: nothing
    """

    if 'userId' not in data: # not login
        # raise ValueError("No userId in given vote.")
        data['userId'] = ""

    if 'type' not in data:
        raise ValueError("No type of vote given.")

    if data['type'] <> "1" and data['type'] <> "-1":
        raise ValueError("Invalid type of vote. Can only be 1 or -1.")

    if 'nodeId' not in data:
        raise ValueError("No nodeId given in vote. Who are you voting on?")

    id_node = Nodes().retrieveById(data['nodeId'])
    if id_node.status_code == 404:
        raise ValueError("Cannot find the node voting on.")


def check_create_event(data):
    """
    Check data of create an event
    :param data:
    :return:
    """

    if 'user_id' not in data:  # user_id empty check
        raise ValueError('No user_id provided in event')

    # TODO user_id user existence check

    if 'node_id' not in data:  # node_id empty check
        raise ValueError('No node_id provided in event')

    # node_id node existence check
    id_node = Nodes().retrieveById(data['node_id'])
    if id_node.status_code == 404:
        raise ValueError('Cannot find the node with id=' + data['node_id'])

    if 'operation' not in data:
        raise ValueError('No operation provided in event')

    if data['operation'] not in PERMITTED_OPERATION_LIST:
        raise ValueError('Operation ' + data['operation'] + ' is not permitted for an event')