## Create an event

Create an event with all the needed fields or modify it, if event with such "_id" already exists.

**URL**: /events
**Method**: POST
**Data constraints**:
Provide all the fields, specified below.

```
{
	"_id": 0, 
	"name": "Not event", 
	"address": "nowhere", 
	"visitors": 0, 
	"openness": "open", 
	"type": 0,
	"start": "2019-10-15 T21:20 +0300",
	"end": "2019-10-15 T21:25 +0300"
}
```
---
## Show all events

Show all events in the database. 
(Convenient for future development)

**URL**: /events
**Method**: GET
**Data constraints**: ```{}```
---
## Create a type of event 

Create a type of event with all the needed fields or modify it, if type of event with such "_id" already exists.

**URL**: /types
**Method**: POST
**Data constraints**:
Provide all the fields, specified below.

```{
	"_id": 0,
	"name": "default" 
}```
---
## Show all types of events

Show all types of events in the database. 
(Convenient for future development)

**URL**: /types
**Method**: GET
**Data constraints**: ```{}```
---
## Show all extra orders

Show all extra orders in the database.
(Convenient for future development)

**URL**: /orders
**Method**: GET
**Data constraints**: ```{}```
---
## Search for events in a timeline

Search for all the events within a specific timeline.

**URL**: /events/search
**Method**: POST
**Data constraints**:
Provide all the fields, specified below.

```{
	"start": "2019-10-15 T21:20 +0300"
	"end": "2019-10-15 T21:25 +0300"
}```
---
## Search for orders in a timeline

Search for all the orders within a specific timeline, including info about corresponding event.

**URL**: /orders/search
**Method**: POST
**Data constraints**:
Provide all the fields, specified below.

```{
	"start": "2019-10-15 T21:20 +0300"
	"end": "2019-10-15 T21:25 +0300"
}```
