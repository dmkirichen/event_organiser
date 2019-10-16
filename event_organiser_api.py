from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from datetime import datetime
import itertools

# Flask default
app = Flask(__name__)
api = Api(app)

# Configuring database side
client = MongoClient('mongodb://localhost:27017/')
db = client['event_organiser']
event_col = db['events']
type_col = db['types']
order_col = db['orders']


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


def is_event_correct(event_json):
    start_dt = datetime.strptime(event_json["start"], "%Y-%m-%d T%H:%M %z")
    end_dt = datetime.strptime(event_json["end"], "%Y-%m-%d T%H:%M %z")
    if start_dt > end_dt:
        return False
    if event_json["visitors"] < 0:
        return False
    type_col.find_one({"name": event_json["type"]})


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


        # Creates new event in the database
        event_col.save(event_json)

        # Creates orders for this event
        create_orders(event_json["_id"])

        return {"you sent": event_json}, 201


class EventTypes(Resource):
    def get(self):
        # Returns all event types in the database
        cursor = type_col.find({})
        doc_dict = dict()
        for i, document in enumerate(cursor):
            doc_dict["type #" + str(i)] = document

        return jsonify(doc_dict)

    def post(self):
        type_json = request.get_json()
        type_col.save(type_json)

        return {'you sent': type_json}, 201


class ExtraOrders(Resource):
    def get(self):
        # Returns all orders in the database
        cursor = order_col.find({})
        doc_dict = dict()
        for i, document in enumerate(cursor):
            doc_dict["order #" + str(i)] = document

        return jsonify(doc_dict)


class EventsSearch(Resource):
    def post(self):
        search_json = request.get_json()
        search_start_dt = datetime.strptime(search_json["start"], "%Y-%m-%d T%H:%M %z")
        search_end_dt = datetime.strptime(search_json["end"], "%Y-%m-%d T%H:%M %z")
        doc_dict = dict()
        counter = itertools.count(start=1)

        for event in event_col.find({}):
            event_start_dt = datetime.strptime(event["start"], "%Y-%m-%d T%H:%M %z")
            event_end_dt = datetime.strptime(event["end"], "%Y-%m-%d T%H:%M %z")

            if search_start_dt < event_start_dt and search_end_dt > event_end_dt:
                doc_dict["event #" + str(counter.__next__())] = event
        return jsonify({"found events": doc_dict})


class OrdersSearch(Resource):
    def post(self):
        search_json = request.get_json()
        search_start_dt = datetime.strptime(search_json["start"], "%Y-%m-%d T%H:%M %z")
        search_end_dt = datetime.strptime(search_json["end"], "%Y-%m-%d T%H:%M %z")
        doc_dict = dict()
        counter = itertools.count(start=1)

        for order in order_col.find({}):
            event = event_col.find_one({"_id": order["event_id"]})
            order_start_dt = datetime.strptime(event["start"], "%Y-%m-%d T%H:%M %z")
            order_end_dt = datetime.strptime(event["end"], "%Y-%m-%d T%H:%M %z")

            if search_start_dt < order_start_dt and search_end_dt > order_end_dt:
                order["name"] = event["name"]
                order["address"] = event["address"]
                doc_dict["order #" + str(counter.__next__())] = order
        return jsonify({"found events": doc_dict})


api.add_resource(Events, '/events')
api.add_resource(EventTypes, '/types')
api.add_resource(ExtraOrders, '/orders')
api.add_resource(EventsSearch, '/events/search')
api.add_resource(OrdersSearch, '/orders/search')

if __name__ == '__main__':
    app.run(debug=True)
