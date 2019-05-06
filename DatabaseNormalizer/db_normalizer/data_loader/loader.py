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

    """Separator for steps ids of path in the temporary tuple in load_airway_details"""
    path_steps_separators = '-'

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
        """Function for get the airports ids from ICAO or IATA code
        :param codes: ICAO or IATA code
        :return: ids of airports
        """
        # Initialization of ids with as many -1 as there are codes
        ids = [-1 for _ in codes]

        # For each airpors save in airport_records
        for airport in self.airport_records:
            # Compare all code in the list codes (if several airports are searched)
            if not any(
                code == airport.icao
                or code == airport.iata \
                for code in codes
            ):
                continue
            
            # If one comparison is correct, we find the airport concerned
            for code in codes:
                if code == airport.icao \
                        or code == airport.iata:
                    ids[codes.index(code)] = airport.id
        
        return ids

    def get_airline_id_from_code(self, code: str) -> int:
        """Function for get the airline id from ICAO or IATA code
        :param code: ICAO or IATA code
        :return: id of airline
        """
        for airline in self.airline_records:
            if code == airline.iata \
                   or code == airline.icao:
                return airline.id
        return -1

    def get_plane_type_from_iata(self, codes: List[str]) -> List[int]:
        """Function for get the plane type ids from ICAO or IATA code
        :param codes: ICAO or IATA code
        :return: ids of plane type
        """
        # Initialization of ids with as many -1 as there are codes. -1 is the default value
        # if the plane type code is not identified
        ids = [-1 for _ in codes]

        # For each plane type save in airport_records
        for plane_type in self.plane_records:
            # Compare all code in the list codes (if several plane type are searched)
            if not any(
                code == plane_type.iata
                for code in codes
            ):
                continue
            
            # If one comparison is correct, we find the airport concerned
            for code in codes:
                if code == plane_type.iata:
                    ids[codes.index(code)] = plane_type.id

        return ids

    def load_airway_details(self):
        """Load airway, step_in, fly_on and use tables since flightnumbers.csv and routes.csv
        """
        # Tuple for save the paths add to airway and fly_on tables
        # And save the combination airline with airway
        # To avoid the duplicates in the tables
        path_ids: Dict[str, Tuple[int, List[int]]] = dict()

        # Initialization of airway_id
        airway_id = NOT_SET

        # Reading of the first file (flightnumbers.csv) with a loop to read line by line
        # And add the datas in the record lists for build the database
        for airline_code, _, stops_icao \
                in self._reader['flight_numbers'].read_content(skip_header=True):

            airline_id = self.get_airline_id_from_code(
                airline_code
            )
            stops_id = ""
            for stop_icao in stops_icao.split(self.path_steps_separators):
                # Get the airport id not in list format
                airport_id, *_ = self.get_airport_ids_from_codes(
                    [stop_icao]
                )
                # If airport_id = -1, we stop the research of ids
                if airport_id == -1:
                    break

                stops_id = (stops_id + str(airport_id)) \
                    if stops_id == "" \
                    else (stops_id + self.path_steps_separators + str(airport_id))

            # We pass this line of flightnumbers.csv if we don't know one airport
            if airport_id == -1:
                continue

            # If the path is know, we take his id
            if stops_id in path_ids:
                if airline_id in path_ids[stops_id][1]:
                    continue
                airway_id, *_ = path_ids[stops_id]
                # Add the airline id at this path
                path_ids[stops_id][1].append(airline_id)

            # Else, we create a new airway
            else:
                # Add the new path in the temporary list
                path_ids[stops_id] = (airway_id, [airline_id])
                airway_id = self.airway_records[-1].id + 1 \
                    if len(self.airway_records) > 0 \
                    else 1
                
                # And, we save this new airway
                self.airway_records.append(
                    Airway(
                        id=airway_id,
                        codeshare=NOT_SET
                    )
                )

                # For each airport in this airway
                rank = 0
                for stop_id in stops_id.split(self.path_steps_separators):
                    # We save the airport in the airway
                    self.step_in_records.append(
                        StepIn(
                            id_airport=int(stop_id),
                            id_airway=airway_id,
                            rank=rank
                        )
                    )
                    rank += 1

            # We link the airline with the airway
            self.use_records.append(
                Use(
                    id_airline=airline_id,
                    id_airway=airway_id
                )
            )

        # Reading of the second file (routes.csv)
        for airline_code, _, airport_src_code, _, airport_dest_code, \
            _, codeshare, stops, plane_iatas \
                in self._reader['routes'].read_content(skip_header=False):

            stops = int(stops)

            # Get the airline id
            airline_id = self.get_airline_id_from_code(airline_code)

            # Get the airport ids not in list format
            airport_src, airport_dst, *_ = self.get_airport_ids_from_codes([
                airport_src_code, 
                airport_dest_code
            ])

            # We pass this line of routes.csv if we don't know one airport
            if airport_src == -1 \
                    or airport_dst == -1:
                continue

            # Get the plane type ids, the plane iata are separated by space in the file
            plane_ids = self.get_plane_type_from_iata([
                plane_iatas.split(' ')
            ])

            # in the temporary list of path,
            if any(
                # a path as: `src-stop-dest` will have only one stop
                len(path.split(self.path_steps_separators)) == stops + 2
                and int(path.split(self.path_steps_separators)[0]) == airport_src
                and int(path.split(self.path_steps_separators)[-1]) == airport_dst
                for path, _ in path_ids.items()
            ):
                # if stops = 0, we know the path, so we can find his id
                if stops == 0:
                    path = str(airport_src) + self.path_steps_separators + str(airport_dst)
                    airway_id, *_ = path_ids[path]
                # else, we search his id in all the temporary list
                else:
                    for path, _ in path_ids.items():
                        if (
                            len(path.split(self.path_steps_separators)) == stops + 2
                            and int(path.split(self.path_steps_separators)[0]) == airport_src
                            and int(path.split(self.path_steps_separators)[-1]) == airport_dst
                        ):
                            airway_id, *_ = path_ids[path]
                            break

                # If the airline is already linked to this airway, we go to the next line of the file
                if airline_id in path_ids[path][1]:
                    continue

                path_ids[path][1].append(airline_id)

            # The associated airway does not exists and has no stops
            elif stops > 0:
                continue

            # We create the new airway
            airway_id = self.airway_records[-1].id + 1 \
                if len(self.airway_records) > 0 \
                else 1

            path_ids[
                self.path_steps_separators.join(
                    (str(airport_src), str(airport_dst))
                )
            ] = (airway_id, [airline_id])

            # airway data recording
            self.airway_records.append(
                Airway(
                    id=airway_id,
                    codeshare=codeshare
                )
            )

            # step_in data recording
            self.step_in_records.append(
                StepIn(
                    id_airport=airport_src,
                    id_airway=airway_id,
                    rank=0
                )
            )

            # step_in data recording
            self.step_in_records.append(
                StepIn(
                    id_airport=airport_dst,
                    id_airway=airway_id,
                    rank=1
                )
            )

            # fly_on data recording
            for plane_id in plane_ids:
                self.fly_on_records.append(
                    FlyOn(
                        id_airway=airway_id,
                        id_plane=plane_id
                    )
                )

                # use data recording
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
