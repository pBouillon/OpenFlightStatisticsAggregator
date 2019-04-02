"""TODO
"""
from typing import List

from db_normalizer.csv_handler.reader import Reader
from db_normalizer.data_loader.utils.table_objects import Airline, Timezone, Use, Airway, City, Country, Dst, FlyOn, \
    Plane, PlaneType, StepIn
from db_normalizer.data_loader.utils.utils import Sources


class Loader:
    """TODO
    """

    def __init__(self):
        """TODO
        """
        self._tables = {
            'airlines': [],
            'airways': [],
            'cities': [],
            'countries': [],
            'dst': [],
            'fly_on': [],
            'planes': [],
            'plane_types': [],
            'step_in': [],
            'timezones': [],
            'use': []
        }
        
        self._content = dict()

        reader = Reader(Sources.airlines)
        self._content['airlines'] = reader.read_content(skip_header=True)

        reader.reload_from(Sources.airports)
        self._content['airports'] = reader.read_content()

        reader.reload_from(Sources.flight_numbers)
        self._content['flight_numbers'] = reader.read_content(skip_header=True)

        reader.reload_from(Sources.planes)
        self._content['planes'] = reader.read_content()

        reader.reload_from(Sources.routes)
        self._content['routes'] = reader.read_content()
        
    def load_airport(self):
        """TODO
        """
        pass

    def load_all(self):
        """TODO
        """
        pass

    def load_dst(self):
        """TODO
        """
        pass

    def load_city(self):
        """TODO
        """
        pass

    def load_country(self):
        """TODO
        """
        pass

    def load_plane(self):
        """TODO
        """
        pass

    def load_plane_type(self):
        """TODO
        """
        pass

    def load_timezone(self):
        """TODO
        """
        pass

    @property
    def airline_records(self) -> List[Airline]:
        """TODO
        """
        return self._tables['airlines']

    @property
    def airway_records(self) -> List[Airway]:
        """TODO
        """
        return self._tables['airways']

    @property
    def city_records(self) -> List[City]:
        """TODO
        """
        return self._tables['cities']

    @property
    def country_records(self) -> List[Country]:
        """TODO
        """
        return self._tables['countries']

    @property
    def dst_records(self) -> List[Dst]:
        """TODO
        """
        return self._tables['dst']

    @property
    def fly_on_records(self) -> List[FlyOn]:
        """TODO
        """
        return self._tables['fly_on']

    @property
    def plane_records(self) -> List[Plane]:
        """TODO
        """
        return self._tables['planes']

    @property
    def plane_type_records(self) -> List[PlaneType]:
        """TODO
        """
        return self._tables['plane_types']

    @property
    def step_in_records(self) -> List[StepIn]:
        """TODO
        """
        return self._tables['step_in']

    @property
    def timezone_records(self) -> List[Timezone]:
        """TODO
        """
        return self._tables['timezones']

    @property
    def use_records(self) -> List[Use]:
        """TODO
        """
        return self._tables['use']
