# Calendar API


This is a back-end ***(REST API)*** for a simple "Calendar" application with 
support for authorization, holidays and the ability to add custom events.
Implemented notification mechanism for upcoming events.


### Authorization:
Implemented simple authorization via email:
- Easy registration via email
- Ability to login via mail
To access data, users authorize and send a token with each
request.

### Custom Events:
Implemented the ability to create custom events with a name
events, start and end dates and times.
If the end date of the event is not specified, consider the end of the day.

Also, when creating an event, it is possible to specify the need
notification of the user about the event in advance.

### User notification of upcoming events:
The notification is implemented through a letter that will be sent to the specified address.
user's mail at the appointed time.

### Getting a list of events:
Implement API for:
- obtaining a list of events per day and a general aggregation by days per month.
- get a list of holidays for the selected month.

### Global holidays support:
It is possible to specify the country in the user profile during registration.
Holidays for the user are given depending on the country selected when
registration.

Full list of countries obtained from the page:
https://www.officeholidays.com/countries/index.php

### Periodic update of the list of holidays:
Implemented periodic updating of the list of holidays

## Technology stack:
The project used the following
technology:
- Python
- Django REST Framework
- Djoser
- Celery
- PostgreSQL
- nginx
- Docker

API response format: *JSON*.

## All in one
How to test this?

- [Install Docker Compose](https://docs.docker.com/compose/install/)
- Clone this repository
- Run all containers with `docker-compose up`