#!/usr/bin/python

import datetime
from db_connect import ConnectDB
from porc import Patch

"""
Nodes class defines all the operations can be done on a (set of) Node(s)
The operations contains:
   operations on a single node: create, update, delete, upvote, downvote, retrieve by ID
   operations on a set of node: retrieve all, retrieve children, retrieve descendant nodes
"""
class Nodes(object):
    __author__ = 'Solki'

    def __init__(self):
        pass

    # create a new node
    # add parent check has been done by service
    #
    def create(self, nodeDisplay, nodeDescription, nodeTags, nodeParents, nodeChildren, nodeVotes, nodeStatus, userId):
        """ Create a new node
        The check of node data has been completed by service

        :param nodeDisplay: display name of a node
        :param nodeDescription: description of a node
        :param nodeTags: tags of a node
        :param nodeParents: parent node ID of this node
        :param nodeChildren: children nodes (if already has)
        :param nodeVotes: votes on node
        :param nodeStatus: status of node
        :param userId: author identification
        :return: a key of the node as an identification
        """

        current_time = datetime.datetime.now()
        conn = ConnectDB().connect()
        node = conn.post('test_nodes', {
            "nodeDisplay": nodeDisplay,
            "nodeDescription": nodeDescription,
            "nodeTags": nodeTags,
            "nodeParents": nodeParents,
            "nodeChildren": nodeChildren,
            "nodeVotes": nodeVotes,  # This can be replaced by invoke methods in vote class
            "nodeStatus": str(nodeStatus),
            "nodeCreateAt": str(current_time),
            "userId": userId
        })

        patch = Patch()
        nodeKey = node.key
        patch.add("_id", node.key)

        conn.patch('test_nodes', node.key, patch)
        print 'nodeKey is ' + node.key

        return nodeKey

    def retrieveById(self, _id):
        """ Retrieve a node by its ID

        :param _id: node ID
        :return: node object
        """
        conn = ConnectDB().connect()
        node = conn.get('test_nodes', _id)
        print node.status_code
        return node

    def retrieveAll(self):
        """ Retrieve all the nodes from database

        :return: array of all the nodes
        """
        conn = ConnectDB().connect()
        nodes = conn.list('test_nodes').all()
        list = []
        for node in nodes:
            list.append(node['value'])
        return list

    def update(self, _id, nodeDisplay, nodeDescription, nodeTags, nodeParents, nodeChildren, nodeVotes, nodeStatus,
               nodeCreateAt, userId):
        """ Update an existing node in database

        :param _id: node ID
        :param nodeDisplay: display name of a node
        :param nodeDescription: description
        :param nodeTags: tags of the node
        :param nodeParents: parent of the node
        :param nodeChildren: children nodes of the node
        :param nodeVotes: votes on the node
        :param nodeStatus: node status
        :param nodeCreateAt: node creation time
        :param userId: user identification
        :return: the key (ID) of the node
        """
        conn = ConnectDB().connect()
        update_result = conn.put('test_nodes', _id, {
            "nodeDisplay": nodeDisplay,
            "nodeDescription": nodeDescription,
            "nodeTags": nodeTags,
            "nodeParents": nodeParents,
            "nodeChildren": nodeChildren,
            "nodeVotes": nodeVotes,  # This can be replaced by invoke methods in vote class
            "nodeStatus": str(nodeStatus),
            "nodeCreateAt": nodeCreateAt,
            "userId": userId,
            "_id": _id
        })

        node_key = update_result.key
        return node_key


    def delete(self, _id):
        """ Delete a node from database

        :param _id: node ID
        :return: nothing
        """
        conn = ConnectDB().connect()
        conn.delete('test_nodes', _id)

    def retrieveChild(self, _id):
        """ Retrieve all direct children nodes of this node

        :param _id: node ID
        :return: all the children nodes of this node
        """
        conn = ConnectDB().connect()
        node = conn.get('test_nodes', _id)
        _list = node['nodeChildren']
        if not _list:
            _list = 'This node has no child'
        return _list

    def retrieveDescendant(self, _id):
        """ Retrieve all the descendant nodes of this node

        :param _id: node ID
        :return: descendant nodes of the node
        """
        conn = ConnectDB().connect()
        node = conn.get('test_nodes', _id)
        _list = node['nodeChildren']
        if not _list:
            _list = 'This node has no descendant node.'
        for child in _list:
            findChild(child, _list, conn)
        return _list

    def upvoteNode(self, node_id, user_id, comment):
        """ Vote up on a node

        :param node_id: ID of node
        :param user_id: ID of user (not required)
        :param comment: Comment on the vote
        :return: node object after voting
        """
        conn = ConnectDB().connect()
        node = conn.get('test_nodes', node_id)
        nodeVotes = node['nodeVotes']
        nodeStatus = int(node['nodeStatus']) + 1
        vote = {'userId': str(user_id), 'type': '1', 'voteDate': str(datetime.datetime.now()), 'comment': comment}
        assert isinstance(nodeVotes, list)
        nodeVotes.append(vote)
        patch = Patch()
        patch.replace('nodeStatus', str(nodeStatus)).replace('nodeVotes', nodeVotes)
        conn.patch('test_nodes', node_id, patch)
        new_node = conn.get('test_nodes', node_id)
        return new_node

    def downvoteNode(self, node_id, user_id, comment):
        """ Voting down on a node

        :param node_id: ID of node
        :param user_id: ID of user (not required)
        :param comment: Comment on the vote
        :return: node object after voting
        """
        conn = ConnectDB().connect()
        node = conn.get('test_nodes', node_id)
        nodeVotes = node['nodeVotes']
        nodeStatus = int(node['nodeStatus']) - 1
        vote = {'userId': str(user_id), 'type': '-1', 'voteDate': str(datetime.datetime.now()), 'comment': comment}
        assert isinstance(nodeVotes, list)
        nodeVotes.append(vote)
        patch = Patch()
        patch.replace('nodeStatus', str(nodeStatus)).replace('nodeVotes', nodeVotes)
        conn.patch('test_nodes', node_id, patch)
        new_node = conn.get('test_nodes', node_id)
        return new_node


def findChild(_id, _list, con):
    node = con.get('test_nodes', _id)
    children = node['nodeChildren']
    if children:
        for child in children:
            _list.append(child)
            findChild(child, _list, con)
