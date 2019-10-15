from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Events(Resource):
    def get(self):
        ...


class EventTypes(Resource):
    def post(self):
        ...


class ExtraOrders(Resource):
    def get(self):
        ...


api.add_resource(Events, '/events/')
api.add_resource(EventTypes, '/types/')
api.add_resource(ExtraOrders, '/orders/')

if __name__ == '__main__':
    app.run()