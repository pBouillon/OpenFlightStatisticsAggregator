# -*- coding: utf-8 -*-
"""
    db_normalizer.data_loader.utils
    -------------------------------

    Store useful data to extract data from the CSV files.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
from typing import List, Dict, Tuple
from db_normalizer.csv_handler.utils import Csv
from db_normalizer.data_loader.enum.loading_strategy import LoadingStrategy


class ExternalSources:
    """External sources data
    """

    """API to fetch countries data"""
    country_api = 'https://restcountries.eu/rest/v2/'

    """special countries to fetch and their search name with their strategy"""
    ambiguous_cities = {
        'Narssarssuaq': (
            'Narsarsuaq',
            LoadingStrategy.DEFAULT
        ),
        'Iles De La Madeleine': (
            'Magdalen_Islands',
            LoadingStrategy.DEFAULT
        ),
        'Portage-la-prairie': (
            'Portage la Prairie',
            LoadingStrategy.DEFAULT
        ),
        'Red Deer Industrial': (
            'Red Deer, Alberta',
            LoadingStrategy.DEFAULT
        ),
        'Riviere Du Loup': (
            'Rivière_du_Loup_(Bas-Saint-Laurent)',
            LoadingStrategy.DEFAULT
        ),
        'Fort Mcpherson': (
            'Fort McPherson',
            LoadingStrategy.DEFAULT
        ),
        'Bejaja': (
            'Béjaïa',
            LoadingStrategy.DEFAULT
        ),
        'Algier': (
            'Algiers',
            LoadingStrategy.DEFAULT
        ),
        'Reggan': (
            'Reggane',
            LoadingStrategy.DEFAULT
        ),
        'Bou Sfer': (
            'Bousfer',
            LoadingStrategy.DEFAULT
        ),
        'Ech-cheliff': (
            'Chlef',
            LoadingStrategy.DEFAULT
        ),
        'Bobo-dioulasso': (
            'Bobo-Dioulasso',
            LoadingStrategy.DEFAULT
        ),
        'Port Hartcourt': (
            'Port_Harcourt',
            LoadingStrategy.DEFAULT
        ),
        'Niatougou': (
            'Niamtougou',
            LoadingStrategy.DEFAULT
        ),
        # FIXME: add more records
    }

    """special countries to fetch and their search name with their strategy"""
    ambiguous_countries = {
        'North Korea': (
            'Korea',
            LoadingStrategy.LEAST_POPULATED
        ),
        'South Korea': (
            'Korea',
            LoadingStrategy.MOST_POPULATED
        ),
        'Congo (Brazzaville)': (
            'Congo',
            LoadingStrategy.LEAST_POPULATED
        ),
        'Congo (Kinshasa)': (
            'Congo',
            LoadingStrategy.MOST_POPULATED
        ),
        'Cape Verde': (
            'Cabo Verde',
            LoadingStrategy.DEFAULT
        ),
        'British Virgin Islands': (
            'Virgin Islands (British)',
            LoadingStrategy.DEFAULT
        )
    }

    """Regex to parse the Wikipedia page's content
        population       when detecting the word `population`
        .*?              ignoring all following characters in a non-greedy way
        (
            \d{1,3}      selecting the next 1 to 3 digits
            (?:,\d{3})+? followed by at least one group as `,NNN`
        )
        (?:\s|<)         ending with a whitespace or a `<`
    """
    city_population_regex = r'population.*?(\d{1,3}(?:,\d{3})+?)(?:\s|<)'

    """"""
    wikipedia_api = 'https://en.wikipedia.org/w/api.php'


class LocalSources:
    """References sources data
    """

    """base folder in which the data files are stored"""
    _base_folder = '../static/data/csv_files/'

    """path to the airports csv file"""
    airports = _base_folder + 'airports' + Csv.ext

    """path to the airlines csv file"""
    airlines = _base_folder + 'airlines' + Csv.ext

    """path to the flight_numbers csv file"""
    flight_numbers = _base_folder + 'flightnumbers' + Csv.ext

    """path to the planes csv file"""
    planes = _base_folder + 'planes' + Csv.ext

    """path to the route csv file"""
    routes = _base_folder + 'routes' + Csv.ext


class CrossReferencesBuffer:
    """Temporary list for reference the codes in files with our ids, to optimize the cross reference
    """

    """Tuple for save the paths add to airway and fly_on tables
    And save the combination airline with airway and plane type
    To avoid the duplicates in the tables"""
    path_ids: Dict[str, Tuple[int, List[int], List[int]]] = dict()

    """link airport iata with id"""
    airport_iata: Dict[str, int] = dict()

    """link airport icao with id"""
    airport_icao: Dict[str, int] = dict()

    """link airline iata with id"""
    airline_iata: Dict[str, int] = dict()

    """save doubled iata for reference at the id in file"""
    airline_iata_double = []

    """link airline id in file with our id"""
    airline_id_file_double: Dict[int, int] = dict()

    """link airline icao with id"""
    airline_icao: Dict[str, int] = dict()

    """link plane type iata with id"""
    plane_type_iata: Dict[str, int] = dict()
    
    """link plane type icao with id"""
    plane_type_icao: Dict[str, int] = dict()
