# -*- coding: utf-8 -*-
"""
    db_normalizer.data_loader.api_external
    --------------------------------------

    TODO doc

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
from http import HTTPStatus

import requests

from db_normalizer.data_loader.utils.table_objects import City, Country, Plane, NOT_SET
from db_normalizer.data_loader.utils.utils import ExternalSources
from db_normalizer.exceptions.api_external_exceptions import UnableToReachCountryApiException


def fill_city(city: City) -> None:
    """TODO doc

    :param city:
    :return:
    """
    # TODO method
    pass


def fill_country(country: Country) -> None:
    """TODO doc

    :param country:
    :return:
    """
    target = f'{ExternalSources.country_api}name/{country.name}'
    target += '?fields=population;area'
    target = url_encode(target)

    # fetch the country's information
    r = requests.get(target)

    # test the API status
    if r.status_code != HTTPStatus.OK:
        raise UnableToReachCountryApiException

    # updating values if possible
    results = r.json()[0]
    country.population = results['area'] if 'area' in results \
        else NOT_SET
    country.population = results['population'] if 'population' in results \
        else NOT_SET


def fill_plane(plane: Plane) -> None:
    """TODO doc

    :param plane:
    :return:
    """
    # TODO: method
    pass


def url_encode(to_sanitize: str) -> str:
    """TODO doc
    """
    # TODO: replace with dict as const (see: https://www.degraeve.com/reference/urlencoding.php)
    return to_sanitize.replace(
        ' ', '%20'
    ).replace(
        ',', '%B4'
    ).replace(
        '\'', '%27'
    ).replace(
        '(', '%28'
    ).replace(
        ')', '%29'
    )
