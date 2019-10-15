from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import datetime

# Flask default
app = Flask(__name__)
api = Api(app)

# Configuring database side
client = MongoClient('mongodb://localhost:27017/')
db = client['event_organiser']
event_col = db['events']
type_col = db['types']
order_col = db['orders']


def create_orders(event_id, num_people, week_day, event_type):
    # Creates all required orders for event
    order_col.delete_many({"event_id": event_id})

    if event_type == "public":
        order_col.save({"event_id": event_id, "type": "medical assistance"})
        order_col.save({"event_id": event_id, "type": "security assistance"})
        order_col.save({"event_id": event_id, "type": "government approval"})

    else:
        if num_people > 50:
            kind = "medical assistance"
            order_col.save({"event_id": event_id, "type": kind})

        if num_people > 20:
            kind = "security assistance"
            order_col.save({"event_id": event_id, "type": kind})

        if week_day not in ("Saturday", "Sunday"):
            kind = "government approval"
            order_col.save({"event_id": event_id, "type": kind})


class Events(Resource):
    def get(self):
        # Returns all events in the database
        cursor = event_col.find({})
        doc_dict = dict()
        for i, document in enumerate(cursor):
            doc_dict["event #" + str(i)] = document

        return jsonify(doc_dict)

    def post(self):
        # Creates new event in the database
        event_json = request.get_json()
        return {"you sent": event_json}, 201


class EventTypes(Resource):
    def get(self):
        # Returns all event types in the database
        cursor = type_col.find({})
        doc_dict = dict()
        for i, document in enumerate(cursor):
            doc_dict["event #" + str(i)] = document

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
            doc_dict["event #" + str(i)] = document

        return jsonify(doc_dict)


api.add_resource(Events, '/events')
api.add_resource(EventTypes, '/types')
api.add_resource(ExtraOrders, '/orders')

if __name__ == '__main__':
    app.run(debug=True)
