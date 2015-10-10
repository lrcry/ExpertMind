__author__ = 'YUN'
from db_connect import ConnectDB


class GenericOperation(object):
    client = ConnectDB().connect()

    def __init__(self, obj):
        self.operate_obj = obj
