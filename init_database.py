from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['event_organiser']

event_col = db['events']
type_col = db['types']
order_col = db['orders']

# Creating default documents for creation of database
posts = [{"_id": 0, "name": "default"},
         {"_id": 1, "name": "public"},
         {"_id": 2, "name": "private"}]
for post in posts:
    type_col.save(post)

posts = [{"_id": 0, "address": "nowhere", "visitors": 0, "openness": "open", "type": 0,
          "start": "2019-10-15 T21:20 +0300",
          "end": "2019-10-15 T21:25 +0300"},
         {"_id": 1, "address": "Kyiv", "visitors": 56, "openness": "open", "type": 2,
          "start": "1997-07-16 T19:20 +0300",
          "end": "1997-07-16 T21:20 +0300"},
         {"_id": 2, "address": "Dnipro", "visitors": 5, "openness": "close", "type": 1,
          "start": "2017-08-16 T19:20 +0300",
          "end": "2017-09-16 T21:20 +0300"}]
for post in posts:
    event_col.save(post)

posts = [{"_id": "0_1", "event_id": 0, "type": "nothing"},
         {"_id": "1_1", "event_id": 1, "type": "medical assistance"},
         {"_id": "2_1", "event_id": 2, "type": "security assistance"}]
for post in posts:
    order_col.save(post)