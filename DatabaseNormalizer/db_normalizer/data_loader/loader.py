from typing import List

from db_normalizer.data_loader.utils.table_objects import Airline, Timezone, Use, Airway, City, Country, Dst, FlyOn, \
    Plane, PlaneType, StepIn


class Loader:

    def __init__(self):
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
            'use': [],
        }

    def load_airport(self):
        pass

    def load_all(self):
        pass

    def load_dst(self):
        pass

    def load_city(self):
        pass

    def load_country(self):
        pass

    def load_plane(self):
        pass

    def load_plane_type(self):
        pass

    def load_timezone(self):
        pass

    @property
    def airline_records(self) -> List[Airline]:
        return self._tables['airlines']

    @property
    def airway_records(self) -> List[Airway]:
        return self._tables['airways']

    @property
    def city_records(self) -> List[City]:
        return self._tables['cities']

    @property
    def country_records(self) -> List[Country]:
        return self._tables['countries']

    @property
    def dst_records(self) -> List[Dst]:
        return self._tables['dst']

    @property
    def fly_on_records(self) -> List[FlyOn]:
        return self._tables['fly_on']

    @property
    def plane_records(self) -> List[Plane]:
        return self._tables['planes']

    @property
    def plane_type_records(self) -> List[PlaneType]:
        return self._tables['plane_types']

    @property
    def step_in_records(self) -> List[StepIn]:
        return self._tables['step_in']

    @property
    def timezone_records(self) -> List[Timezone]:
        return self._tables['timezones']

    @property
    def use_records(self) -> List[Use]:
        return self._tables['use']
