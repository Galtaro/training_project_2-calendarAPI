from distutils.util import strtobool

from django_filters import rest_framework as filters, ChoiceFilter
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import CustomUser
from events.models import Event, STATUS_CHOICES
from events.serializers import ListCreateApiEventSerializer
from events.utils.create_tasks import create_task_send_notification


class EventFilter(filters.FilterSet):
    from_datetime = filters.DateTimeFilter(
        field_name='start_datetime',
        lookup_expr='gte'
    )
    to_datetime = filters.DateTimeFilter(
        field_name='end_datetime',
        lookup_expr='lte'
    )
    official_holiday = ChoiceFilter(
        choices=STATUS_CHOICES,
        empty_label='Show all events'
    )

    class Meta:
        model = Event
        fields = ['official_holiday']

    def filter_queryset(self, queryset):
        user = self.request.user
        if 'official_holiday' in self.data:
            official_holiday = self.data['official_holiday']
            if user.country and len(official_holiday):
                official_holiday = strtobool(official_holiday)
                queryset = Event.objects.filter(
                    user=user,
                    official_holiday=official_holiday
                )
        return queryset


class ListCreateApiEvent(ListCreateAPIView):
    serializer_class = ListCreateApiEventSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter

    def get_queryset(self):
        queryset = Event.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=(self.request.user, ))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        event_name = serializer.validated_data['name']
        notification = serializer.validated_data['notification'].value_time
        event_start_datetime = serializer.validated_data['start_datetime']
        email = self.request.user.email
        user = CustomUser.objects.get(email=request.user)
        user.save()
        if notification:
            create_task_send_notification(
                event_name=event_name,
                notification=notification,
                event_start_datetime=event_start_datetime,
                email=email
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
