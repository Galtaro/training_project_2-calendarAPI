from django.urls import path

from accounts.views import ActivateUser

urlpatterns = [
    path('activate/<uid>/<token>', ActivateUser.as_view({'get': 'activation'}), name='activation'),
]
