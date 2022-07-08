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
        self.assertTrue(queryset_countries)

    def test_remote_url(self):
        status_code = urllib.request.urlopen(
            'https://www.officeholidays.com/countries').getcode()
        self.assertEqual(status_code, status.HTTP_200_OK)

    def test_get_all_countries(self):
        call_command('create_country')
        response = requests.get('https://www.officeholidays.com/countries')
        soup = BeautifulSoup(response.text, 'lxml')
        countries = soup.find_all('div', class_='four omega columns')[0].find_all('a')
        self.assertIsNone(Country.objects.get(id=1).country_name)
        self.assertEqual(len(Country.objects.all()), len(countries) + 1)

