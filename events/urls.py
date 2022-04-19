from django.urls import path

from events.views import ListCreateApiEvent

app_name = "Event"

urlpatterns = [
    path(
        'list_create/',
        ListCreateApiEvent.as_view(),
        name='list-create-event'
    ),

]