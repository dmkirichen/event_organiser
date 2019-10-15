from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['event_organiser']

event_col = db['events']
type_col = db['types']
order_col = db['orders']

print(event_col.count())
print(type_col.count())
print(order_col.count())
