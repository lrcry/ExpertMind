__author__ = 'YUN'

from db_connect import ConnectDB
from porc import Patch
import json


class User(object):
    user_json = {}

    def __init__(self, given_name, surname, email):
        self.given_name = given_name
        self.surname = surname
        self.email = email

    # Translate user object to json
    def to_json(self):
        self.user_json = json.dumps(self, default=lambda o: o.__dict__)

    # def create_user(self):
    #     self.to_json()
    #     response = self.client.post('users', self.user_json)
    #     response = self.client.post(object.m)
    #     print response

    # Create a user record to db
    # Return True if insert record success, else return False
    def create(self):
        client = ConnectDB().connect()
        response = client.post('users', {
            "given_name": self.given_name,
            "surname": self.surname,
            "email": self.email
        })
        status = response.status_code
        reason = response.reason
        if status == 201:
            patch = Patch()
            patch.add("_id", response.key)
            client.patch('users', response.key, patch)
            result = {"result": "success", "message": reason}
            return result
        else:
            result = {"result": "failed", "message": reason}
            return result

    # Retrieve a specific user by user key
    # Return a user json if find, else return None
    @staticmethod
    def retrieveById(user_key):
        client = ConnectDB().connect()
        response = client.get('users', user_key)
        status = response.status_code
        if status == 200:
            return response.json
        else:
            return None

    # Retrieve a specific user by user email
    # Email is unique for each user
    @staticmethod
    def retrieveByEmail(email):
        client = ConnectDB().connect()
        user_list =[]
        users = client.search('users', 'email:'+email).all()[0]['value']
        # for user in users:
        #     value = user['value']
        #     user_list.append(value)
        return users


    # Retrieve all users
    # Return a list of users (json)
    @staticmethod
    def retrieveAll():
        client = ConnectDB().connect()
        user_list = []
        user_list_response = client.list('users').all()
        for user_res in user_list_response:
            value = user_res['value']
            user_list.append(value)
        return user_list

    # Update a specific user with user key and a user object
    # Return result msg (json)
    @staticmethod
    def update(user_key, user):
        client = ConnectDB().connect()
        response = client.put('users', user_key, {
            "_id": user_key,
            "given_name": user.given_name,
            "surname": user.surname,
            "email": user.email
        })
        status = response.status_code
        reason = response.reason
        if status == 201:
            result = {"result": "success", "message": reason}
            return result
        else:
            result = {"result": "failed", "message": reason}
            return result

    # delete_user a specific user with key
    @staticmethod
    def delete(user_key):
        user = User.retrieveById(user_key)
        if None == user:
            result = {"result": "failed", "message": "user doesn't exist"}
            return result
        client = ConnectDB().connect()
        response = client.delete('users', user_key)
        user = User.retrieveById(user_key)
        if None == user:
            result = {"result": "success", "message": "success"}
            return result
        else:
            reason = response.reason
            result = {"result": "failed", "message": reason}
            return result

