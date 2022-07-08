from django.core.management import call_command
from django.test import TestCase

from accounts.models import Country


class TestCountry(TestCase):

    def test_string_representation_of_the_country_instance(self):
        call_command('create_country')
        country_1 = Country.objects.get(pk=1)
        country_2 = Country.objects.get(pk=2)
        self.assertEqual(str(country_1), 'None')
        self.assertEqual(str(country_2), country_2.country_name)
