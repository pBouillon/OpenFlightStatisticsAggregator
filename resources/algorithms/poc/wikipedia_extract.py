# -*- coding: utf-8 -*-
"""
    wikipedia_city_big_numbers_extract.py
    -------------------------------------
    Extract huge numbers that may be the population (further treatment needed) from a wikipedia city's page.
    :author: Bouillon Pierre
"""
import re
import requests

from http import HTTPStatus


API = 'https://en.wikipedia.org/w/api.php'
LOOK_FOR = 'Goroka'
POPULATION_REGEX = r'.*?(?:population).*?(\d{1,3}(?:,\d{3})+?)+(?:\s|<)'


def main():
    target = f'{API}?action=parse&page={LOOK_FOR}&format=json'
    r = requests.get(target)

    if r.status_code != HTTPStatus.OK:
        exit('Can\'t reach the API')

    data = r.json()['parse']['text']['*']
    print(re.findall(POPULATION_REGEX, data, flags=re.IGNORECASE))


if __name__ == '__main__':
    main()
