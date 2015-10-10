__author__ = 'YUN'

from db_connect import ConnectDB
from porc import Patch

class Vote(object):
    def __init__(self, vote_type, description, vote_user, vote_at, vote_on_node):
        self.type = vote_type
        self.description = description
        self.voteUser = vote_user
        self.voteAt = vote_at
        self.voteOnNode = vote_on_node

    # Create a vote record to db
    # Return True if insert vote record success, else False
    def create(self):
        client = ConnectDB().connect()
        response = client.post('votes', {
            "type": self.type,
            "description": self.description,
            "voteUser": self.voteUser,
            "voteAt": self.voteAt,
            "voteOnNode": self.voteOnNode
        })
        status = response.status_code
        reason = response.reason
        if status == 201:
            patch = Patch()
            patch.add("_id", response.key)
            client.patch('votes', response.key, patch)
            result = {"result": "success", "message": reason}
            return result
        else:
            result = {"result": "failed", "message": reason}
            return result

    # Retrieve vote by vote key
    # Return vote json if find, else return None
    @staticmethod
    def retrieveById(vote_key):
        client = ConnectDB().connect()
        response = client.get('votes', vote_key)
        status = response.status_code
        if status == 200:
            return response.json
        else:
            return None

    # Retrieve all vote
    # Return a list of vote (json)
    @staticmethod
    def retrieveAll():
        client = ConnectDB().connect()
        vote_list =[]
        vote_list_response = client.list('votes').all()
        for vote_res in vote_list_response:
            value = vote_res['value']
            vote_list.append(value)
        return vote_list

    # Update a specific vote with vote key and a vote object
    # Return result msg (json)
    @staticmethod
    def update(vote_key, vote):
        client = ConnectDB().connect()
        response = client.put('votes', vote_key, {
            "_id": vote_key,
            "type": vote.type,
            "description": vote.description,
            "voteUser": vote.voteUser,
            "voteAt": vote.voteAt,
            "voteOnNode": vote.voteOnNode
        })
        status = response.status_code
        reason = response.reason
        if status == 201:
            result = {"result": "success", "message": reason}
            return result
        else:
            result = {"result": "failed", "message": reason}
            return result

    # delete a specific vote with vote_key
    @staticmethod
    def delete(vote_key):
        vote = Vote.retrieveById(vote_key)
        if None == vote:
            result = {"result": "failed", "message": "vote doesn't exist"}
            return result
        client = ConnectDB().connect()
        response = client.delete('votes', vote_key)
        vote = Vote.retrieveById(vote_key)
        if None == vote:
            result = {"result": "success", "message": "success"}
            return result
        else:
            reason = response.reason
            result = {"result": "failed", "message": reason}
            return result

    # Retrieve votes for a specific node key and vote type
    # Return the vote number
    @staticmethod
    def retrieve_numb_vote_by_node_id(node_key, vote_type):
        client = ConnectDB().connect()
        vote_list = client.search('votes', 'voteOnNode:'+node_key + ' AND type:'+vote_type).all()
        return len(vote_list)
