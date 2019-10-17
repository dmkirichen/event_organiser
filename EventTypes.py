"""
Author: Kyrychenko Dmytro
Date: 17 Oct 2019

Class EventTypes.
This class gives user an option to see all types of events in the database.
Also it allows to add new ones.
"""

from pymongo import MongoClient
from flask import request, jsonify
from flask_restful import Resource

# Configuring database side
client = MongoClient('mongodb://localhost:27017/')
db = client['event_organiser']
type_col = db['types']


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
