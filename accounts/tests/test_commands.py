import urllib.request

from django.test import TestCase
import requests
from bs4 import BeautifulSoup
from django.core.management import call_command
from rest_framework import status

from accounts.models import Country


class TestCreateCountry(TestCase):

    def test_call_command(self):
        call_command('create_country')
        queryset_countries = Country.objects.all()

        """Checking the creation of instances of the Country class in the database"""

        self.assertTrue(queryset_countries)

    def test_remote_url(self):
        status_code = urllib.request.urlopen(
            'https://www.officeholidays.com/countries').getcode()

        """Checking the availability of a remote address"""

        self.assertEqual(status_code, status.HTTP_200_OK)

    def test_get_all_countries(self):
        call_command('create_country')
        response = requests.get('https://www.officeholidays.com/countries')
        soup = BeautifulSoup(response.text, 'lxml')
        countries = soup.find_all('div', class_='four omega columns')[0].find_all('a')

        """Checking for the creation of an empty instance of the Country class"""

        self.assertIsNone(Country.objects.get(pk=1).country_name)

        """Checking the creation of all records of instances of the Country class 
        that are available at a remote address"""

        self.assertEqual(len(Country.objects.all()), len(countries) + 1)

