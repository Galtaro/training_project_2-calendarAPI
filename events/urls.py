from django.urls import path

from events.views import CreateApiEvent

app_name = "Event"

urlpatterns = [
    path('create/', CreateApiEvent.as_view(), name='create-event'),

]