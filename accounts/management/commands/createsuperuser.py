from django.contrib.auth.management.commands import createsuperuser
from django.core import exceptions

from accounts.models import Country


class Command(createsuperuser.Command):

    """
    The get_input_data method is overridden, when creating superuser it was not possible to
    set the country directly, since this field is a Foreign key field.
    After overriding the method, when creating superuser, you do not need to enter the country,
    since it will be set by default
    """

    def get_input_data(self, field, message, default=None):
        if message == 'Country (Country.id): ':
            return Country.objects.get(id=1)
        raw_value = input(message)
        if default and raw_value == '':
            raw_value = default
        try:
            val = field.clean(raw_value, None)
        except exceptions.ValidationError as e:
            self.stderr.write("Error: %s" % '; '.join(e.messages))
            val = None

        return val

