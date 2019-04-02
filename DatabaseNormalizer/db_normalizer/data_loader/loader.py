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
        self._preload_content()

    def _preload_content(self):
        """TODO

        FIXME: use generator and not lists (generator copy or altervative)
        """
        reader = Reader(Sources.airlines)

        def extract_content_from(source: str, skip: bool = False):
            reader.reload_from(source)
            return list(reader.read_content(skip))

        self._content['airlines'] = extract_content_from(
            source=Sources.airlines,
            skip=True
        )

        self._content['airports'] = extract_content_from(
            source=Sources.airports
        )

        self._content['flight_numbers'] = extract_content_from(
            source=Sources.flight_numbers,
            skip=True
        )

        self._content['planes'] = extract_content_from(
            source=Sources.planes
        )

        self._content['routes'] = extract_content_from(
            source=Sources.routes
        )

    def load_airport(self):
        """TODO
        """
        pass

    def load_all(self):
        """TODO
        """
        # first, load table with no references to others
        self.load_dst()
        self.load_airway()

    def load_airway(self):
        """TODO
        """
        for _, _, _, _, _, \
                _, codeshare, *_ in self._content['routes']:
            self.airway_records.append(
                Airway(
                    id=self.airway_records[-1].id + 1
                    if len(self.airway_records) > 0
                    else 1,
                    codeshare=codeshare
                )
            )

    def load_dst(self):
        """TODO
        """
        dst_names = set()

        for _, _, _, _, _, \
                _, _, _, _, _, \
                dst_name, *_ in self._content['airports']:
            dst_names.add(dst_name)

        for dst_name in dst_names:
            self.dst_records.append(
                Dst(
                    id=self.dst_records[-1].id + 1
                    if len(self.dst_records) > 0
                    else 1,
                    name=dst_name
                )
            )

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
