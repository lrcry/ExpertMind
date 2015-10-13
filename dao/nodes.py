#!/usr/bin/python

import datetime
from db_connect import ConnectDB
from porc import Patch


class Nodes(object):
    __author__ = 'Solki'

    def __init__(self):
        pass

    # add parent check has been done by service
    def create(self, nodeDisplay, nodeDescription, nodeTags, nodeParents, nodeChildren, nodeVotes, nodeStatus):
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
            "nodeCreateAt": str(current_time)
        })

        patch = Patch()
        nodeKey = node.key
        patch.add("_id", node.key)

        conn.patch('test_nodes', node.key, patch)
        print 'nodeKey is ' + node.key

        return nodeKey

    def retrieveById(self, _id):
        conn = ConnectDB().connect()
        node = conn.get('test_nodes', _id)
        print node.status_code
        return node

    def retrieveAll(self):
        conn = ConnectDB().connect()
        nodes = conn.list('test_nodes').all()
        list = []
        for node in nodes:
            list.append(node['value'])
        return list

    def update(self, _id, nodeDisplay, nodeDescription, nodeTags, nodeParents, nodeChildren, nodeVotes, nodeStatus,
               nodeCreateAt):
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
            "_id": _id
        })

        nodeKey = update_result.key
        return nodeKey

    def delete(self, _id):
        conn = ConnectDB().connect()
        conn.delete('test_nodes', _id)

    # update the corresponding table like votes, nodes who are parents or children of the deleted node

    def retrieveChild(self, _id):
        conn = ConnectDB().connect()
        node = conn.get('test_nodes', _id)
        _list = node['nodeChildren']
        if not _list:
            _list = 'This node has no child'
        return _list

    def retrieveDescendant(self, _id):
        conn = ConnectDB().connect()
        node = conn.get('test_nodes', _id)
        _list = node['nodeChildren']
        if not _list:
            _list = 'This node has no descendant node.'
        for child in _list:
            findChild(child, _list, conn)
        return _list

    def upvoteNode(self, node_id, user_id, comment):
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
