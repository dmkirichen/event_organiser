from pymongo import MongoClient
import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['event_organiser']

event_col = db['events']
type_col = db['types']
order_col = db['orders']

# Creating default documents for creation of database
post = {"_id": 0, "name": "default"}
type_col.save(post)

post = {"_id": 0, "address": "nowhere", "visitors": 0, "openness": "open", "type": 0,
        "start": datetime.datetime.now().utcnow(), "end": datetime.datetime.now().utcnow()}
event_col.save(post)

post = {"_id": 0, "event_id": 0, "type": "nothing"}
order_col.save(post)