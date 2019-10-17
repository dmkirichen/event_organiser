"""
Author: Kyrychenko Dmytro
Date: 17 Oct 2019

Class Events and all the needed functions.
This class gives user an option to see all events in the database.
Also it allows to add new ones.
"""

from pymongo import MongoClient
from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime
import itertools

# Configuring database side
client = MongoClient('mongodb://localhost:27017/')
db = client['event_organiser']
event_col = db['events']
type_col = db['types']
order_col = db['orders']


def is_event_correct(event_json):
    start_dt = datetime.strptime(event_json["start"], "%Y-%m-%d T%H:%M %z")
    end_dt = datetime.strptime(event_json["end"], "%Y-%m-%d T%H:%M %z")
    if start_dt > end_dt:
        return False
    if event_json["visitors"] < 0:
        return False
    if type_col.find_one({"_id": event_json["type"]}) == {}:
        return False
    return True


def create_orders(event_id):
    # Creates all required orders for event
    event = event_col.find_one({"_id": event_id})
    num_people = event["visitors"]
    event_type = event["type"]

    start_dt = datetime.strptime(event["start"], "%Y-%m-%d T%H:%M %z")
    end_dt = datetime.strptime(event["end"], "%Y-%m-%d T%H:%M %z")

    weekdays = False  # flag to know if event will be on Mon-Fri

    if start_dt.weekday() not in [5, 6] or \
            end_dt.weekday() not in [5, 6] or \
            (end_dt - start_dt).days > 2:
        weekdays = True

    order_col.delete_many({"event_id": event_id})
    counter = itertools.count(start=1)

    # If it is 'public' event, we should have all extra orders
    public_id = type_col.find_one({"name": "public"})["_id"]
    if event_type == public_id:
        order_col.save({"_id": str(event_id) + "_" + str(counter.__next__()),
                        "event_id": event_id, "type": "medical assistance"})
        order_col.save({"_id": str(event_id) + "_" + str(counter.__next__()),
                        "event_id": event_id, "type": "security assistance"})
        order_col.save({"_id": str(event_id) + "_" + str(counter.__next__()),
                        "event_id": event_id, "type": "government approval"})

    # If it is not, we will have only those orders, that we need
    else:
        if num_people > 50:
            kind = "medical assistance"
            order_col.save({"_id": str(event_id) + "_" + str(counter.__next__()),
                            "event_id": event_id, "type": kind})

        if num_people > 20:
            kind = "security assistance"
            order_col.save({"_id": str(event_id) + "_" + str(counter.__next__()),
                            "event_id": event_id, "type": kind})

        if weekdays:
            kind = "government approval"
            order_col.save({"_id": str(event_id) + "_" + str(counter.__next__()),
                            "event_id": event_id, "type": kind})


class Events(Resource):
    def get(self):
        # Returns all events in the database
        cursor = event_col.find({})
        doc_dict = dict()
        for i, document in enumerate(cursor):
            doc_dict["event #" + str(i)] = document

        return jsonify(doc_dict)

    def post(self):
        event_json = request.get_json()

        # Checks correctness of the events
        if not is_event_correct(event_json):
            return {"error": "your event has unappropriate fields"}

        # Creates new event in the database
        event_col.save(event_json)

        # Creates orders for this event
        create_orders(event_json["_id"])

        return {"you sent": event_json}, 201
