from bs4 import BeautifulSoup
import requests
from django.core.management.base import BaseCommand

from accounts.models import Country


def get_all_countries(*args, **kwargs):

    """
    The None element in the list is needed to be able to create an entry in the Country
    table with an empty country_name attribute by default.
    """

    countries_list = ["", ]
    page = "https://www.officeholidays.com/countries"
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'lxml')
    countries = soup.find_all('div', class_='four omega columns')[0].find_all('a')
    for country in countries:
        countries_list.append(country.contents[1].strip())
    return countries_list


class Command(BaseCommand):

    def handle(self, *args, **options):
        countries = get_all_countries()
        for country in countries:
            Country.objects.create(country_name=country)
