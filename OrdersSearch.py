"""
Author: Kyrychenko Dmytro
Date: 17 Oct 2019

Class OrdersSearch and all the needed functions.
This class gives user an option to find all orders in the specific timelinem
and displays info about connected event.
"""

from pymongo import MongoClient
from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime
from itertools import count

# Configuring database side
client = MongoClient('mongodb://localhost:27017/')
db = client['event_organiser']
event_col = db['events']
order_col = db['orders']


def is_timeline_correct(time_json):
    start_dt = datetime.strptime(time_json["start"], "%Y-%m-%d T%H:%M %z")
    end_dt = datetime.strptime(time_json["end"], "%Y-%m-%d T%H:%M %z")
    if end_dt < start_dt:
        return False
    return True


class OrdersSearch(Resource):
    def post(self):
        search_json = request.get_json()
        if not is_timeline_correct(search_json):
            return {"error": "your timeline is not correct"}
        search_start_dt = datetime.strptime(search_json["start"], "%Y-%m-%d T%H:%M %z")
        search_end_dt = datetime.strptime(search_json["end"], "%Y-%m-%d T%H:%M %z")
        doc_dict = dict()
        counter = count(start=1)

        for order in order_col.find({}):
            event = event_col.find_one({"_id": order["event_id"]})
            order_start_dt = datetime.strptime(event["start"], "%Y-%m-%d T%H:%M %z")
            order_end_dt = datetime.strptime(event["end"], "%Y-%m-%d T%H:%M %z")

            if search_start_dt < order_start_dt and search_end_dt > order_end_dt:
                order["name"] = event["name"]
                order["address"] = event["address"]
                doc_dict["order #" + str(counter.__next__())] = order
        return jsonify({"found events": doc_dict})
