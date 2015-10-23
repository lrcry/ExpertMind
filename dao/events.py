import datetime
from db_connect import ConnectDB
from porc import Patch


__author__ = 'hansmong'


"""
Events class defines all supported operations on Events with static method of class
The operation contains:
    create a new event
    retrieve all the events
    retrieve an event by ID
    retrieve events by user ID and node ID
"""


class Events(object):

    @staticmethod
    def create(event):
        """
        Create a new event object
        :param event:
        :return:
        """
        print 'create'
        db_conn = ConnectDB().connect()
        current_time = datetime.datetime.now()  # create_at
        event['create_at'] = str(current_time)
        event['status'] = 'EVENT_UNREAD'
        event_create = db_conn.post('node_events', event)

        # append a key as ID to event
        patch = Patch()
        event_key = event_create.key
        patch.add("_id", event_key)
        db_conn.patch('node_events', event_key, patch)
        print 'event_key=' + event_key

        return event_key

    # TODO update an event (mainly for status)

    @staticmethod
    def retrieve_all():
        """
        Retrieve all the events from database
        :return: json array of events
        """
        print 'retrieve all'
        db_conn = ConnectDB().connect()
        events = db_conn.list('node_events').all()
        events_list = []
        for event in events:
            events_list.append(event['value'])

        return events_list

    @staticmethod
    def retrieve_by_id(_id):
        """
        Retrieve an event by its id
        :param _id: event id
        :return: event object
        """
        print 'retrieve by event id'

        db_conn = ConnectDB().connect()
        event = db_conn.get('node_events', _id)
        print event.status_code

        return event