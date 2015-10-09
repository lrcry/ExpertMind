__author__ = 'YUN'

from porc import Patch
from db_connect import ConnectDB


class Tag(object):
    def __init__(self, tag_name, tag_description, created_by, created_at):
        self.tagName = tag_name
        self.tagDescription = tag_description
        self.createdBy = created_by
        self.createdAt = created_at

    def create(self):
        client = ConnectDB().connect()
        response = client.post('tags', {
            "tagName": self.tagName,
            "tagDescription": self.tagDescription,
            "createdBy": self.createdBy,
            "createdAt": self.createdAt
        })
        status = response.status_code
        reason = response.reason
        if status == 201:
            patch = Patch()
            patch.add("_id", response.key)
            client.patch('tags', response.key, patch)
            result = {"result": "success", "message": reason}
            return result
        else:
            result = {"result": "failed", "message": reason}
            return result

    # Retrieve a specific tag by tag_key
    # Return a tag json if find, else return None
    @staticmethod
    def retrieveById(tag_key):
        client = ConnectDB().connect()
        response = client.get('tags', tag_key)
        status = response.status_code
        if status == 200:
            return response.json
        else:
            return None

    # Retrieve all tags
    # Return a list of tags (json)
    @staticmethod
    def retrieveAll():
        client = ConnectDB().connect()
        tag_list = []
        tag_list_response = client.list('tags').all()
        for tag_res in tag_list_response:
            value = tag_res['value']
            tag_list.append(value)
        return tag_list

    # Update a specific tag with tag key and a tag object
    # Return result msg (json)
    @staticmethod
    def update(tag_key, tag):
        client = ConnectDB().connect()
        response = client.put('tags', tag_key, {
            "_id": tag_key,
            "tagName": tag.tagName,
            "tagDescription": tag.tagDescription,
            "createdBy": tag.createdBy,
            "createdAt": tag.createdAt
        })
        status = response.status_code
        reason = response.reason
        if status == 201:
            result = {"result": "success", "message": reason}
            return result
        else:
            result = {"result": "failed", "message": reason}
            return result

    # delete a specific tag with tag_key
    @staticmethod
    def delete(tag_key):
        tag = Tag.retrieveById(tag_key)
        if None == tag:
            result = {"result": "failed", "message": "tag doesn't exist"}
            return result
        client = ConnectDB().connect()
        response = client.delete('tags', tag_key)
        tag = Tag.retrieveById(tag_key)
        if None == tag:
            result = {"result": "success", "message": "success"}
            return result
        else:
            reason = response.reason
            result = {"result": "failed", "message": reason}
            return result
