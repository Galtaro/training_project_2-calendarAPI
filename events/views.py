from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from events.serializers import CreateApiEventSerializer


class CreateApiEvent(CreateAPIView):
    serializer_class = CreateApiEventSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
