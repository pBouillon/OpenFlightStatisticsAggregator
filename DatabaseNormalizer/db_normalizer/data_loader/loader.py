# -*- coding: utf-8 -*-
"""
    db_normalizer.data_loader.loader
    -------------------------------

    Extract and store data contained in the .csv files.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
from typing import List, Dict, Tuple

from db_normalizer.csv_handler.reader import Reader
from db_normalizer.csv_handler.utils import Csv
from db_normalizer.data_loader.api_external import fill_country, fill_city
from db_normalizer.data_loader.utils.table_objects \
    import Airline, Timezone, Use, Airway, City, Country, Dst, FlyOn, \
    Plane, PlaneType, StepIn, NOT_SET, Airport
from db_normalizer.data_loader.utils.utils import LocalSources, ExternalSources
from db_normalizer.exceptions.api_external_exceptions import ResourceNotFoundException


class Loader:
    """References Loader

    Load and extract data from .csv files.
    """

    def __init__(self):
        """Constructor
        """
        # records of each table
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

        # reader for each source file
        self._reader = {
            'airlines': Reader(LocalSources.airlines),
            'airports': Reader(LocalSources.airports),
            'flight_numbers': Reader(LocalSources.flight_numbers),
            'planes': Reader(LocalSources.planes),
            'routes': Reader(LocalSources.routes),
        }

    def load_all_raw(self):
        """Load all data

        First load airways data
        Then all geographical and plane data
        Finally tables with references to others (foreign keys)
        """
        # standalone tables
        self.load_airway()

        # group loading
        self.load_geographical_data()
        self.load_plane_data()

        # table with references to others
        self.load_airline()

    def load_airline(self):
        """Load airlines data
        """
        # unwrapping relevant data from the source file
        for _, name, alias, iata, icao, \
            callsign, _, active, *_ \
                in self._reader['airlines'].read_content(skip_header=True):
            # create an airline from the extracted data and add it to
            # the stored records
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
                    is_active=True if active == 'Y' else False,
                    name=name
                )
            )

    def load_airway(self):
        """Load airway data
        """
        # unwrapping relevant data from the source file
        for _, _, _, _, _, \
            _, codeshare, *_ \
                in self._reader['routes'].read_content():
            # create an airway from the extracted data and add it to
            # the stored records
            self.airway_records.append(
                Airway(
                    id=self.airway_records[-1].id + 1
                    if len(self.airway_records) > 0
                    else 1,
                    codeshare=codeshare
                )
            )

    def load_external(self, smooth: bool = False) -> None:
        """Load additional data for all records that need it

        First load external data for the country records
        Then load external data for the city records
        Finally load external data for the plane records
        """
        self.load_external_country(smooth)
        self.load_external_city(smooth)
        self.load_external_plane(smooth)

    def load_external_country(self, smooth: bool) -> None:
        """Load additional data for each recorded country from external sources

        :param smooth: silence exception if True; otherwise, raise it
        :raise ResourceNotFoundException: on an unfetchable data queried
        """
        # some countries can lead to several results
        for i in range(len(self.country_records)):
            # if the country has a special name for the API
            if self.country_records[i].name \
                    in ExternalSources.ambiguous_countries:
                # fetching the parameters allowing the search
                search_name, strategy = ExternalSources.ambiguous_countries[
                    self.country_records[i].name
                ]
                original_name = self.country_records[i].name

                # updating the country for the search
                self.country_records[i].name = search_name
                try:
                    fill_country(
                        self.country_records[i],
                        strategy
                    )
                except ResourceNotFoundException as rnfe:
                    if not smooth:
                        raise rnfe
                # restore original value
                self.country_records[i].name = original_name

            else:
                try:
                    fill_country(self.country_records[i])
                except ResourceNotFoundException as rnfe:
                    if not smooth:
                        raise rnfe

    def load_external_city(self, smooth: bool) -> None:
        """Load additional data for each recorded city from external sources

        :param smooth: silence exception if True; otherwise, raise it
        :raise ResourceNotFoundException: on an unfetchable data queried
        """
        for i in range(len(self.city_records)):
            # if the country has a special name for the API
            if self.city_records[i].name \
                    in ExternalSources.ambiguous_countries:
                # fetching the parameters allowing the search
                search_name, strategy = ExternalSources.ambiguous_cities[
                    self.city_records[i].name
                ]
                original_name = self.city_records[i].name

                # updating the country for the search
                self.city_records[i].name = search_name
                try:
                    fill_city(
                        self.city_records[i],
                        strategy
                    )
                except ResourceNotFoundException as rnfe:
                    if not smooth:
                        raise rnfe
                # restore original value
                self.city_records[i].name = original_name

            else:
                try:
                    fill_city(self.city_records[i])
                except ResourceNotFoundException as rnfe:
                    if not smooth:
                        raise rnfe

    def load_external_plane(self, smooth: bool) -> None:
        """Load additional data for each recorded plane from external sources

        :param smooth: silence exception if True; otherwise, raise it
        :raise ResourceNotFoundException: on an unfetchable data queried
        """
        pass

    def load_geographical_data(self):
        """Load geographical data

        Creates airport, city, country, dst, timezone records
        """
        # countries['name'] = [country_id, dst_id]
        countries: Dict[str, List[int]] = dict()
        country_id = 1

        # dst['name'] = id
        dst: Dict[str, int] = dict()
        dst_id = 1

        # timezones['name'] = (timezone_id, padding)
        timezones: Dict[str, Tuple[int, int]] = dict()

        # unwrapping relevant data from the source file
        for _, airport_name, city_name, country_name, airport_iata, \
            airport_icao, airport_long, airport_lat, airport_alt, padding, \
            dst_name, timezone_name, *_ \
                in self._reader['airports'].read_content():
            # extract dst data
            if dst_name not in dst.keys():
                dst[dst_name] = dst_id
                dst_id += 1

            # extract country data if it's not a duplicate
            if country_name not in countries.keys():
                countries[country_name] = [country_id, dst_id]
                country_id += 1

            # extract timezone data if it's not a duplicate
            if timezone_name not in timezones:
                timezones[timezone_name] = (len(timezones), padding)

            # extract city data
            self.city_records.append(
                City(
                    id=self.city_records[-1].id + 1
                    if len(self.city_records) > 0
                    else 1,
                    id_country=countries[country_name][0],
                    id_timezone=timezones[timezone_name][0],
                    name=city_name
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
                    longitude=float(airport_long),
                    latitude=float(airport_lat),
                    altitude=float(airport_alt)
                )
            )

        # store country records
        for name, data in countries.items():
            country_id, dst_id = data
            self.country_records.append(
                Country(
                    id=country_id,
                    id_dst=dst_id,
                    name=name
                )
            )

        # store timezone records
        for name, data in timezones.items():
            timezone_id, padding = data
            self.timezone_records.append(
                Timezone(
                    id=timezone_id,
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
        """Load load plane data

        Depending on the provided data, create a Plane or a Plane
        """
        # unwrapping relevant data from the source file
        for model, iata, icao, *_ \
                in self._reader['planes'].read_content():
            # records with no ico are a PlaneType
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
                    ))
            else:
                self.plane_type_records.append(
                    PlaneType(
                        id=self.plane_type_records[-1].id + 1
                        if len(self.plane_type_records) > 0
                        else 1,
                        type=model,
                        iata=iata
                    ))

    @property
    def airline_records(self) -> List[Airline]:
        """Getter for `_tables['airlines']`
        :return: the airline records
        """
        return self._tables['airlines']

    @property
    def airport_records(self) -> List[Airport]:
        """Getter for `_tables['airports']`
        :return: the airports records
        """
        return self._tables['airports']

    @property
    def airway_records(self) -> List[Airway]:
        """Getter for `_tables['airways']`
        :return: the airways records
        """
        return self._tables['airways']

    @property
    def city_records(self) -> List[City]:
        """Getter for `_tables['cities']`
        :return: the cities records
        """
        return self._tables['cities']

    @property
    def country_records(self) -> List[Country]:
        """Getter for `_tables['countries']`
        :return: the countries records
        """
        return self._tables['countries']

    @property
    def dst_records(self) -> List[Dst]:
        """Getter for `_tables['dst']`
        :return: the dst records
        """
        return self._tables['dst']

    @property
    def fly_on_records(self) -> List[FlyOn]:
        """Getter for `_tables['fly_on']`
        :return: the fly_on records
        """
        return self._tables['fly_on']

    @property
    def plane_records(self) -> List[Plane]:
        """Getter for `_tables['planes']`
        :return: the planes records
        """
        return self._tables['planes']

    @property
    def plane_type_records(self) -> List[PlaneType]:
        """Getter for `_tables['plane_types']`
        :return: the plane_types records
        """
        return self._tables['plane_types']

    @property
    def records(self) -> int:
        """Getter for the number of stored records
        :return: the total of the stored records
        """
        return sum(len(records) for _, records in self._tables.items())

    @property
    def step_in_records(self) -> List[StepIn]:
        """Getter for `_tables['step_in']`
        :return: the step_in records
        """
        return self._tables['step_in']

    @property
    def timezone_records(self) -> List[Timezone]:
        """Getter for `_tables['timezones']`
        :return: the timezones records
        """
        return self._tables['timezones']

    @property
    def use_records(self) -> List[Use]:
        """Getter for `_tables['use']`
        :return: the use records
        """
        return self._tables['use']
