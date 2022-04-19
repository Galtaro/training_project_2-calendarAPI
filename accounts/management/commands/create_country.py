from bs4 import BeautifulSoup
import requests
from django.core.management.base import BaseCommand

from accounts.models import Country


def get_all_countries(*args, **kwargs):

    """
    An empty entry in the Country database table is needed to prevent
    the user from entering a country during registration
    """

    Country.objects.create(country_name=None)
    page = "https://www.officeholidays.com/countries"
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'lxml')
    countries = soup.find_all('div', class_='four omega columns')[0].find_all('a')
    objs = (Country(country_name=country.contents[1].strip()) for country in countries)
    Country.objects.bulk_create(objs)


class Command(BaseCommand):

    def handle(self, *args, **options):
        get_all_countries()


