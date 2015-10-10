__author__ = 'YUN'

from db_connect import ConnectDB
from porc import Patch


class Add(object):
    def __init__(self, node, add_at):
        self.node = node
        self.addAt = add_at

    def create(self):
        client = ConnectDB().connect()
        response = client.post('adds', {
            "node": self.node,
            "addAt": self.addAt
        })
        status = response.status_code
        reason = response.reason
        if status == 201:
            patch = Patch()
            patch.add("_id", response.key)
            client.patch('adds', response.key, patch)
            result = {"result": "success", "message": reason}
            return result
        else:
            result = {"result": "failed", "message": reason}
            return result

    @staticmethod
    def retrieveById(add_key):
        client = ConnectDB().connect()
        response = client.get('adds', add_key)
        status = response.status_code
        if status == 200:
            return response.json
        else:
            return None

    @staticmethod
    def retrieveAll():
        client = ConnectDB().connect()
        add_list =[]
        add_list_response = client.list('adds').all()
        for add_res in add_list_response:
            value = add_res['value']
            add_list.append(value)
        return add_list

    @staticmethod
    def update(add_key, add):
        client = ConnectDB().connect()
        response = client.put('adds', add_key, {
            "_id": add_key,
            "node": add.node,
            "addAt": add.addAt
        })
        status = response.status_code
        reason = response.reason
        if status == 201:
            result = {"result": "success", "message": reason}
            return result
        else:
            result = {"result": "failed", "message": reason}
            return result

    @staticmethod
    def delete(add_key):
        add = Add.retrieveById(add_key)
        if None == add:
            result = {"result": "failed", "message": "add doesn't exist"}
            return result
        client = ConnectDB().connect()
        response = client.delete('adds', add_key)
        add = Add.retrieveById(add_key)
        if None == add:
            result = {"result": "success", "message": "success"}
            return result
        else:
            reason = response.reason
            result = {"result": "failed", "message": reason}
            return result



