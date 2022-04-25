from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.signals import add_official_holidays_to_custom_user

"""
There’s code to handle user activation, but it doesn’t support a GET request
- Created custom view inherited from Djoser UserViewSet to handle incoming GET request.
- Override activation method to accept parameters of uid token included in URL and remove 
@actiondecorator which only allowed HTTP POST.
- Override the get_serializer method to insert the uid and token value uid token into its kwargs['data'].
- Defined a URL pattern that maps our ACTIVATION_URL fetch request to the official modern representation.
"""


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        # this line is the only change from the base implementation.

        kwargs['data'] = {"uid": self.kwargs['uid'], "token": self.kwargs['token']}

        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiCustomUserEvent(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        response = add_official_holidays_to_custom_user(user)
        return response

