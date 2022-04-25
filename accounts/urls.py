from django.urls import path

from accounts.views import ActivateUser, ApiCustomUserEvent

urlpatterns = [
    path('activate/<uid>/<token>',
         ActivateUser.as_view({'get': 'activation'}),
         name='activation'
         ),
    path('account/update_official_holidays',
         ApiCustomUserEvent.as_view(),
         name='update-custom-user-event'
         )
]
