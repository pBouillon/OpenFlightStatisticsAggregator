from db_normalizer.csv_handler.utils import Csv


class Sources:
    _base_folder = '../static/data/csv_files/'

    airports = _base_folder + 'airports' + Csv.ext

    airlines = _base_folder + 'airlines' + Csv.ext

    flight_numbers = _base_folder + 'flightnumbers' + Csv.ext

    planes = _base_folder + 'planes' + Csv.ext

    routes = _base_folder + 'routes' + Csv.ext
