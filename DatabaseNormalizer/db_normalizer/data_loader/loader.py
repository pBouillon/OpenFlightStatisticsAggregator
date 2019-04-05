"""TODO
"""
from typing import List

from db_normalizer.csv_handler.reader import Reader
from db_normalizer.csv_handler.utils import Csv
from db_normalizer.data_loader.utils.table_objects import Airline, Timezone, Use, Airway, City, Country, Dst, FlyOn, \
    Plane, PlaneType, StepIn, NOT_SET, Airport
from db_normalizer.data_loader.utils.utils import Sources


class Loader:
    """TODO
    """

    def __init__(self):
        """TODO
        """
        self._tables = {
            'airlines': [],
            'airports': [],
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

        self._reader = {
            'airlines': Reader(Sources.airlines),
            'airports': Reader(Sources.airports),
            'flight_numbers': Reader(Sources.flight_numbers),
            'planes': Reader(Sources.planes),
            'routes': Reader(Sources.routes),
        }

    def load_all(self):
        """TODO
        """
        # standalone tables
        self.load_airway()

        # group loading
        self.load_geographical_data()
        self.load_plane_data()

        # table with references to others
        self.load_airline()

    def load_airline(self):
        """TODO
        """
        for _, name, alias, iata, icao,\
            callsign, _, active, *_ \
                in self._reader['airlines'].read_content(skip_header=True):
            self.airline_records.append(
                Airline(
                    id=self.airline_records[-1].id + 1
                    if len(self.airline_records) > 0
                    else 1,
                    alias=alias,
                    callsign=callsign,
                    iata=iata,
                    icao=icao,
                    id_country=NOT_SET,
                    is_active=active,
                    name=name
                )
            )

    def load_airway(self):
        """TODO
        """
        for _, _, _, _, _, \
                _, codeshare, *_ \
                in self._reader['routes'].read_content():
            self.airway_records.append(
                Airway(
                    id=self.airway_records[-1].id + 1
                    if len(self.airway_records) > 0
                    else 1,
                    codeshare=codeshare
                )
            )

    def load_geographical_data(self):
        """TODO
        """
        countries = dict()
        dst = dict()
        timezones = dict()

        country_id = 1
        dst_id = 1
        for _, airport_name, city_name, country_name, airport_iata, \
                airport_icao, airport_long, airport_lat, airport_alt, padding, \
                dst_name, timezone_name, *_ \
                in self._reader['airports'].read_content():
            # extract dst data
            if dst_name not in dst.keys():
                dst[dst_name] = dst_id
                dst_id += 1

            # extract country data
            if country_name not in countries.keys():
                countries[country_name] = [country_id, dst_id]
                country_id += 1

            # extract timezone data
            if timezone_name not in timezones:
                timezones[timezone_name] = padding

            # extract city data
            self.city_records.append(
                City(
                    id=self.city_records[-1].id + 1
                    if len(self.city_records) > 0
                    else 1,
                    id_country=countries[country_name][0],
                    id_timezone=timezones[timezone_name],
                    name=city_name,
                    population=NOT_SET
                )
            )

            # extract airport data
            self.airport_records.append(
                Airport(
                    id=self.airport_records[-1].id + 1
                    if len(self.airport_records) > 0
                    else 1,
                    id_city=self.city_records[-1].id,
                    name=airport_name,
                    iata=airport_iata,
                    icao=airport_icao,
                    longitude=airport_long,
                    latitude=airport_lat,
                    altitude=airport_alt
                )
            )

        # store country records
        for name, data in countries.items():
            country_id, dst_id = data
            self.country_records.append(
                Country(
                    id=country_id,
                    id_dst=dst_id,
                    name=name,
                    population=NOT_SET,
                    area=NOT_SET
                )
            )

        # store timezone records
        for name, padding in timezones.items():
            self.timezone_records.append(
                Timezone(
                    id=self.timezone_records[-1].id + 1
                    if len(self.timezone_records) > 0
                    else 1,
                    name=name,
                    padding=float(padding)
                )
            )

        # store dst records
        for name, dst_id in dst.items():
            self.dst_records.append(
                Dst(id=dst_id, name=name)
            )

    def load_plane_data(self):
        """TODO
        """
        for model, iata, icao, *_ \
                in self._reader['planes'].read_content():
            if icao != Csv.null_value:
                self.plane_records.append(
                    Plane(
                        id=self.plane_records[-1].id + 1
                        if len(self.plane_records) > 0
                        else 1,
                        id_plane_type=NOT_SET,
                        icao=icao,
                        iata=iata,
                        model=model,
                        passenger=NOT_SET,
                        fret=NOT_SET,
                        speed=NOT_SET,
                        consumption=NOT_SET
                    )
                )

            else:
                self.plane_type_records.append(
                    PlaneType(
                        id=self.plane_type_records[-1].id + 1
                        if len(self.plane_type_records) > 0
                        else 1,
                        type=model,
                        iata=iata
                    )
                )

    @property
    def airline_records(self) -> List[Airline]:
        """TODO
        """
        return self._tables['airlines']

    @property
    def airport_records(self) -> List[Airport]:
        """TODO
        """
        return self._tables['airports']

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
    def records(self) -> int:
        """TODO

        :return:
        """
        return sum(len(records) for _, records in self._tables.items())

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
