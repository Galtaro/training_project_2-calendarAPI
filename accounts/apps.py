from django.apps import AppConfig
from djoser.signals import user_registered


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from . import signals
        from accounts.models import CustomUser

        user_registered.connect(signals.add_official_holidays_to_custom_user, sender=CustomUser)
