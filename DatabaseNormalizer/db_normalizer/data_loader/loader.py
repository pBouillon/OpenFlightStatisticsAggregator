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

    def get_airport_ids_from_codes(self, codes: List[str]) -> List[int]:
        """TODO: doc
        """
        # TODO: doc
        ids = [-1 for _ in codes]

        # TODO: doc
        for airport in self.airport_records:
            # TODO: doc
            if not any(
                code == airport.icao
                or code == airport.iata \
                for code in codes
            ):
                continue
            
            # TODO: doc
            for code in codes:
                if code == airport.icao \
                        or code == airport.iata:
                    ids[codes.index(code)] = airport.id
        
        return ids

    def get_airline_id_from_code(self, code: str) -> int:
        """TODO: doc
        """
        for airline in self.airline_records:
            if code == airline.iata \
                   or code == airline.icao:
                return airline.id
        return -1

    def get_plane_type_from_iata(self, codes: List[str]) -> List[int]:
        """TODO: doc
        """
        # TODO: doc
        ids = [-1 for _ in codes]

        # TODO: doc
        for plane_type in self.plane_records:
            # TODO: doc
            if not any(
                code == plane_type.iata
                for code in codes
            ):
                continue
            
            # TODO: doc
            for code in codes:
                if code == plane_type.iata:
                    ids[codes.index(code)] = plane_type.id

        return ids

    def load_airway_details(self):
        """TODO: doc
        Enregistrement des ids dans path_ids au lieu des ICAO
        """
        # TODO: doc
        path_ids: Dict[str, Tuple[int, int]] = dict()

        # TODO: doc
        airway_id = NOT_SET

        # TODO: doc
        for airline_code, _, stops_icao \
                in self._reader['flight_numbers'].read_content(skip_header=True):

            airline_id = self.get_airline_id_from_code(
                airline_code
            )

            # TODO: doc
            if stops_icao in path_ids:
                airway_id, _ = path_ids[stops_icao]

            # TODO: doc
            else:
                airway_id = self.airway_records[-1].id + 1 \
                    if len(self.airway_records) > 0 \
                    else 1
                
                # TODO: doc
                self.airway_records.append(
                    Airway(
                        id=airway_id,
                        codeshare=NOT_SET
                    )
                )

                # TODO: doc
                rank = 0
                for stop_icao in stops_icao.split('-'):
                    # TODO: doc
                    airport_id, *_ = self.get_airport_ids_from_codes(
                        [stop_icao]
                    )

                    self.step_in_records.append(
                        StepIn(
                            id_airport=airport_id,
                            id_airway=airway_id,
                            rank=rank
                        )
                    )
                    rank += 1
                
                # TODO: doc
                path_ids[stops_icao] = (airway_id, airline_id)

            # TODO: doc
            self.use_records.append(
                Use(
                    id_airline=airline_id,
                    id_airway=airway_id
                )
            )

        # TODO: doc
        for airline_code, _, airport_src_code, _, airport_dest_code, \
            _, codeshare, stops, plane_iatas \
                in self._reader['routes'].read_content(skip_header=False):

            # TODO: doc
            airport_src, airport_dst, *_ = self.get_airport_ids_from_codes([
                airport_src_code, 
                airport_dest_code
            ])

            # TODO: doc
            plane_ids = self.get_plane_type_from_iata([
                plane_iatas.split(' ')
            ])

            # TODO: doc
            if any(
                # a path as: `src-stop-dest` will have only one stop
                len(path.split('-')) == int(stops) + 2
                and path.split('-')[0] == airport_src_code
                and path.split('-')[-1] == airport_dest_code
                for path, _ in path_ids.items()
            ):
                airway_id = -1  # TODO: code

            # the associated airway does not exists and has no stops
            elif not stops:
                # TODO: doc
                airway_id = self.airway_records[-1].id + 1 \
                    if len(self.airway_records) > 0 \
                    else 1

                path_ids[
                    '-'.join((airport_src, airport_dst))
                ] = (
                    airway_id,
                    self.get_airline_id_from_code(airline_code)
                )
                
                # TODO: doc
                self.airway_records.append(
                    Airway(
                        id=self.airway_records[-1].id,
                        codeshare=codeshare
                    )
                )

                # TODO: doc
                self.step_in_records.append(
                    StepIn(
                        id_airport=airport_src,
                        id_airway=self.airway_records[-1].id,
                        rank=0
                    )
                )

                # TODO: doc
                self.step_in_records.append(
                    StepIn(
                        id_airport=airport_dst,
                        id_airway=self.airway_records[-1].id,
                        rank=1
                    )
                )

            # TODO: doc
            for plane_id in plane_ids:
                self.fly_on_records.append(
                    FlyOn(
                        id_airway=airway_id,
                        id_plane=plane_id
                    )
                )

            airline_id = self.get_airline_id_from_code(airline_code)

            # TODO: doc
            if any(
                data[1] == airline_id
                and len(path.split('-')) == int(stops) + 2
                and path.split('-')[0] == airport_src_code
                and path.split('-')[-1] == airport_dest_code
                for path, data in path_ids.items()
            ):
                continue
            
            # TODO: doc
            path_ids[
                '-'.join((airport_src, airport_dst))
            ] = (airway_id, airline_id)

            self.use_records.append(
                Use(
                    id_airway=airway_id,
                    id_airline=airline_id
                )
            )

    def load_airline(self):
        """Load airlines data
        """
        # unwrapping relevant data from the source file
        for _, name, alias, iata, icao, \
            callsign, country, active, *_ \
                in self._reader['airlines'].read_content(skip_header=True):
            # create an airline from the extracted data and add it to
            # research id country
            id_country = NOT_SET
            for country_record in self.country_records:
                if country == country_record.name:
                    id_country = country_record.id

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
                    id_country=id_country,
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

    def load_all_raw(self):
        """Load all data

        First load airways data
        Then all geographical and plane data
        Finally tables with references to others (foreign keys)
        """
        # group loading
        self.load_geographical_data()
        self.load_plane_data()

        # table with references to others
        self.load_airline()

        # linking table
        self.load_airway_details()

    def load_external(self, smooth: bool = False) -> None:
        """Load additional data for all records that need it

        First load external data for the country records
        Then load external data for the city records
        Finally load external data for the plane records
        """
        self.load_external_country(smooth)
        self.load_external_city(smooth)

    def load_external_city(self, smooth: bool) -> None:
        """Load additional data for each recorded city from external sources

        :param smooth: silence exception if True; otherwise, raise it
        :raise ResourceNotFoundException: on an unfetchable data queried
        """
        for i in range(len(self.city_records)):
            # if the country has a special name for the API
            if self.city_records[i].name \
                    in ExternalSources.ambiguous_cities:
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
