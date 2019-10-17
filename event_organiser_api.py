"""
Author: Kyrychenko Dmytro
Date: 17 Oct 2019

Main skeleton of the API.
"""

from flask import Flask
from flask_restful import Api
from pymongo import MongoClient
from OrdersSearch import OrdersSearch
from EventsSearch import EventsSearch
from ExtraOrders import ExtraOrders
from EventTypes import EventTypes
from Events import Events


# Flask default
app = Flask(__name__)
api = Api(app)

# Configuring database side
client = MongoClient('mongodb://localhost:27017/')
db = client['event_organiser']
event_col = db['events']
type_col = db['types']
order_col = db['orders']


api.add_resource(Events, '/events')
api.add_resource(EventTypes, '/types')
api.add_resource(ExtraOrders, '/orders')
api.add_resource(EventsSearch, '/events/search')
api.add_resource(OrdersSearch, '/orders/search')

if __name__ == '__main__':
    app.run(debug=True)
