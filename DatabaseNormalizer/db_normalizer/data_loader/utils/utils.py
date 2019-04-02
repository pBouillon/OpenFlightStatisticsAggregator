from db_normalizer.csv_handler.utils import Csv


class Sources:
    """TODO
    """

    """TODO
    """
    _base_folder = '../static/data/csv_files/'

    """TODO
    """
    airports = _base_folder + 'airports' + Csv.ext

    """TODO
    """
    airlines = _base_folder + 'airlines' + Csv.ext

    """TODO
    """
    flight_numbers = _base_folder + 'flightnumbers' + Csv.ext

    """TODO
    """
    planes = _base_folder + 'planes' + Csv.ext

    """TODO
    """
    routes = _base_folder + 'routes' + Csv.ext
