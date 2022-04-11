from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from events.management.commands.create_official_holidays import get_official_holidays
from events.serializers import CreateApiEventSerializer
from events.utils.create_tasks import create_task_send_notification


class CreateApiEvent(CreateAPIView):
    serializer_class = CreateApiEventSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=(self.request.user, ))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        event_name = serializer.validated_data["name"]
        notification = serializer.validated_data["notification"].value_time
        event_start_datetime = serializer.validated_data["start_datetime"]
        email = self.request.user.email
        if notification:
            create_task_send_notification(
                event_name=event_name,
                notification=notification,
                event_start_datetime=event_start_datetime,
                email=email
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

