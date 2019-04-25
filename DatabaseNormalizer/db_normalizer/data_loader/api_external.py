# -*- coding: utf-8 -*-
"""
    db_normalizer.data_loader.api_external
    --------------------------------------

    Toolbox to load missing data from several table structures

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
import urllib.parse
from http import HTTPStatus

import requests

from db_normalizer.data_loader.enum.loading_strategy import LoadingStrategy
from db_normalizer.data_loader.utils.table_objects import City, Country, Plane, NOT_SET, EXTERNAL_DATA
from db_normalizer.data_loader.utils.utils import ExternalSources
from db_normalizer.exceptions.api_external_exceptions import UnableToReachCountryApiException, ResourceNotFoundException


def fill_city(
        city: City,
        strategy: LoadingStrategy = LoadingStrategy.DEFAULT
) -> None:
    """TODO doc

    :param city:
    :param strategy:
    :return:
    """
    # TODO method
    pass


def fill_country(
        country: Country,
        strategy: LoadingStrategy = LoadingStrategy.DEFAULT
) -> None:
    """Fill the missing values of a country depending on its name

    :param country: country object to complete
    :param strategy: on several records fetched, adopt the specified strategy
    :raise ConnectionError: on request timeout
    :raise ResourceNotFoundException: on request failure
    """
    # don't query the API if not needed
    if country.area != EXTERNAL_DATA \
            and country.population != EXTERNAL_DATA:
        return

    # build the request
    target = ExternalSources.country_api
    target += 'name/'
    target += urllib.parse.quote(country.name)  # encode special chars
    target += '?fields=population;area'

    # fetch the country's information
    try:
        r = requests.get(target)
    except ConnectionError:
        raise UnableToReachCountryApiException

    # test the API status
    if r.status_code != HTTPStatus.OK:
        raise ResourceNotFoundException

    # selecting the appropriate result
    results = r.json()
    if strategy == LoadingStrategy.DEFAULT:
        results = results[0]
    elif strategy == LoadingStrategy.LEAST_POPULATED:
        results = min(results, key=lambda row: row['population'])
    elif strategy == LoadingStrategy.MOST_POPULATED:
        results = max(results, key=lambda row: row['population'])

    # updating values if possible
    country.area = results['area'] if 'area' in results \
        else NOT_SET
    country.population = results['population'] if 'population' in results \
        else NOT_SET


def fill_plane(
        plane: Plane,
        strategy: LoadingStrategy = LoadingStrategy.DEFAULT
) -> None:
    """TODO doc

    :param plane:
    :param strategy:
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
