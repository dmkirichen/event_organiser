"""
Author: Kyrychenko Dmytro
Date: 17 Oct 2019

Class ExtraOrders.
This class gives user an option to see all extra orders in the database.
"""

from pymongo import MongoClient
from flask import jsonify
from flask_restful import Resource

# Configuring database side
client = MongoClient('mongodb://localhost:27017/')
db = client['event_organiser']
order_col = db['orders']


class ExtraOrders(Resource):
    def get(self):
        # Returns all orders in the database
        cursor = order_col.find({})
        doc_dict = dict()
        for i, document in enumerate(cursor):
            doc_dict["order #" + str(i)] = document

        return jsonify(doc_dict)