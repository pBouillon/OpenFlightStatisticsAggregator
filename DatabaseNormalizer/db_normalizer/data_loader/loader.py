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
from db_normalizer.data_loader.utils.utils import LocalSources, ExternalSources, CrossReferencesBuffer
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

    @staticmethod
    def get_airport_ids_from_codes(codes: List[str]) -> List[int]:
        """Function for get the airports ids from ICAO or IATA code
        :param codes: ICAO or IATA code
        :return: ids of airports
        """
        ids = []
        # we test the size of the codes to know their type and searched in the right list
        for code in codes:
            if len(code) == 3 \
                    and code in CrossReferencesBuffer.airport_iata:
                ids.append(CrossReferencesBuffer.airport_iata[code])
            elif len(code) == 4 \
                    and code in CrossReferencesBuffer.airport_icao:
                ids.append(CrossReferencesBuffer.airport_icao[code])
            else:
                ids.append(-1)

        return ids

    @staticmethod
    def get_airline_id_from_code(code: str, id_file: int) -> int:
        """Function for get the airline id from ICAO or IATA code
        :param code: ICAO or IATA code
        :param id_file: id in file (route.csv)
        :return: id of airline
        """

        # we test the size of the code to know its type and searched in the right list
        if len(code) == 2 \
                and code in CrossReferencesBuffer.airline_iata:
            # if the code is a doubled iata, we must refer to the ids in the file
            if code in CrossReferencesBuffer.airline_iata_double:
                if id_file in CrossReferencesBuffer.airline_id_file_double:
                    return CrossReferencesBuffer.airline_id_file_double[id_file]
                return -1
            else:
                return CrossReferencesBuffer.airline_iata[code]
        elif len(code) == 3 \
                and code in CrossReferencesBuffer.airline_icao:
            return CrossReferencesBuffer.airline_icao[code]
        else:
            return -1

    @staticmethod
    def get_plane_type_from_codes(codes: List[str]) -> List[int]:
        """Function for get the plane type ids from ICAO or IATA code
        :param codes: ICAO or IATA code
        :return: ids of plane type
        """
        ids = []
        # we test the size of the codes to know their type and searched in the right list
        for code in codes:
            if len(code) == 3 \
                    and (code in CrossReferencesBuffer.plane_iata
                         or code in CrossReferencesBuffer.plane_type_iata):
                # if the code refers to the type of plane, we must link all plane ids of this type
                if code in CrossReferencesBuffer.plane_type_iata:
                    for plane_id in CrossReferencesBuffer.plane_type_iata[code]:
                        ids.append(plane_id)
                else:
                    ids.append(CrossReferencesBuffer.plane_iata[code])
            elif len(code) == 4 \
                    and code in CrossReferencesBuffer.plane_icao:
                ids.append(CrossReferencesBuffer.plane_icao[code])
            else:
                ids.append(-1)

        return ids

    def load_airway_details(self):
        """Load airway, step_in, fly_on and use tables since flightnumbers.csv and routes.csv
        """

        # Reading of the first file (flightnumbers.csv) with a loop to read line by line
        # And add the datas in the record lists for build the database
        for airline_code, _, stops_icao \
                in self._reader['flight_numbers'].read_content(skip_header=True):

            airline_id = self.get_airline_id_from_code(airline_code, -1)
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
            if stops_id in CrossReferencesBuffer.path_ids:
                # If the airline is already registered for this path,
                # we go to the next line of the file because there is no information to add
                if airline_id in CrossReferencesBuffer.path_ids[stops_id][1]:
                    continue

                airway_id, *_ = CrossReferencesBuffer.path_ids[stops_id]
                # Add the airline id at this path
                CrossReferencesBuffer.path_ids[stops_id][1].append(airline_id)

            # Else, we create a new airway
            else:
                airway_id = self.airway_records[-1].id + 1 \
                    if len(self.airway_records) > 0 \
                    else 1

                # Add the new path in the temporary list
                CrossReferencesBuffer.path_ids[stops_id] = (airway_id, [], [])
                
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
                            id=self.step_in_records[-1].id + 1
                            if len(self.step_in_records) > 0
                            else 1,
                            id_airport=int(stop_id),
                            id_airway=airway_id,
                            rank=rank
                        )
                    )
                    rank += 1

            if airline_id == -1:
                continue

            CrossReferencesBuffer.path_ids[stops_id][1].append(airline_id)
            # We link the airline with the airway
            self.use_records.append(
                Use(
                    id_airline=airline_id,
                    id_airway=airway_id
                )
            )

        # Reading of the second file (routes.csv)
        for airline_code, airline_id_file, airport_src_code, _, airport_dest_code, \
            _, codeshare, stops, plane_iatas \
                in self._reader['routes'].read_content(skip_header=False):
            stops = int(stops)

            # Get the airline id
            airline_id = self.get_airline_id_from_code(airline_code, airline_id_file)

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
            plane_ids = self.get_plane_type_from_codes(
                plane_iatas.split(' ')
            )

            path = str(airport_src) + self.path_steps_separators + str(airport_dst)
            # if stops = 0, we know the path, so we can find his id
            if stops == 0 \
                    and path in CrossReferencesBuffer.path_ids:
                airway_id, *_ = CrossReferencesBuffer.path_ids[path]

            # if stops > 0, we don't know, but we can find a path of the same size, same airport source
            # and same airport destinaition which is very likely to be the desired path
            elif stops > 0:
                if any(
                    # a path as: `src-stop-dest` will have only one stop
                    len(path.split(self.path_steps_separators)) == stops + 2
                    and int(path.split(self.path_steps_separators)[0]) == airport_src
                    and int(path.split(self.path_steps_separators)[-1]) == airport_dst
                    for path, _ in CrossReferencesBuffer.path_ids.items()
                ):
                    # We search his id in all the temporary list
                    for path, _ in CrossReferencesBuffer.path_ids.items():
                        if (
                            len(path.split(self.path_steps_separators)) == stops + 2
                            and int(path.split(self.path_steps_separators)[0]) == airport_src
                            and int(path.split(self.path_steps_separators)[-1]) == airport_dst
                        ):
                            airway_id, *_ = CrossReferencesBuffer.path_ids[path]
                            break

                # we pass the paths of which we do not know the intermediate steps
                # and which have no resemblance with the known path
                else:
                    continue

            else:
                # We create the new airway
                airway_id = self.airway_records[-1].id + 1 \
                    if len(self.airway_records) > 0 \
                    else 1

                CrossReferencesBuffer.path_ids[
                    self.path_steps_separators.join(
                        (str(airport_src), str(airport_dst))
                    )
                ] = (airway_id, [], [])

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
                        id=self.step_in_records[-1].id + 1
                        if len(self.step_in_records) > 0
                        else 1,
                        id_airport=airport_src,
                        id_airway=airway_id,
                        rank=0
                    )
                )

                # step_in data recording
                self.step_in_records.append(
                    StepIn(
                        id=self.step_in_records[-1].id + 1
                        if len(self.step_in_records) > 0
                        else 1,
                        id_airport=airport_dst,
                        id_airway=airway_id,
                        rank=1
                    )
                )

            # fly_on data recording
            for plane_id in plane_ids:
                # save data if we know id and not already recorded
                if plane_id == -1 \
                        or plane_id in CrossReferencesBuffer.path_ids[path][2]:
                    continue
                CrossReferencesBuffer.path_ids[path][2].append(plane_id)
                self.fly_on_records.append(
                    FlyOn(
                        id_airway=airway_id,
                        id_plane=plane_id
                    )
                )

            if airline_id == -1 \
                    or airline_id in CrossReferencesBuffer.path_ids[path][1]:
                continue

            CrossReferencesBuffer.path_ids[path][1].append(airline_id)
            # use data recording
            self.use_records.append(
                Use(
                    id_airline=airline_id,
                    id_airway=airway_id
                )
            )

    def load_airline(self):
        """Load airlines data
        """
        # unwrapping relevant data from the source file
        for airline_id, name, alias, iata, icao, \
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

            # Add iata and icao in the temporary list, to facilitate cross-referencing
            if iata != "" and iata != "\\N" and iata != "-" and iata != "N/A":
                # The iata can be doubled, so we have to register the duplicate and use the file identifiers instead
                if iata in CrossReferencesBuffer.airline_iata:
                    CrossReferencesBuffer.airline_iata_double.append(iata)
                    CrossReferencesBuffer.airline_id_file_double[iata] = int(airline_id)
                else:
                    CrossReferencesBuffer.airline_iata[iata] = self.airline_records[-1].id
            if icao != "" and icao != "\\N" and icao != "-" and icao != "N/A":
                CrossReferencesBuffer.airline_icao[icao] = self.airline_records[-1].id

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

            # Add iata and icao in the temporary list, to facilitate cross-referencing
            if airport_iata != "" and airport_iata != "\\N" and airport_iata != "-" and airport_iata != "N/A":
                CrossReferencesBuffer.airport_iata[airport_iata] = self.airport_records[-1].id

            if airport_icao != "" and airport_icao != "\\N" and airport_icao != "-" and airport_icao != "N/A":
                CrossReferencesBuffer.airport_icao[airport_icao] = self.airport_records[-1].id

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
            # In first time, we record only the plane
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

                CrossReferencesBuffer.plane_name[model] = self.plane_records[-1].id
                # Add iata and icao in the temporary list, to facilitate cross-referencing
                if iata != "" and iata != "\\N" and iata != "-" and iata != "N/A":
                    CrossReferencesBuffer.plane_iata[iata] = self.plane_records[-1].id
                if icao != "" and icao != "\\N" and icao != "-" and icao != "N/A":
                    CrossReferencesBuffer.plane_icao[icao] = self.plane_records[-1].id

        for model, iata, icao, *_ \
                in self._reader['planes'].read_content():

            # In second time, we record the plane type and link them with plane in temporary list
            if icao == Csv.null_value:
                self.plane_type_records.append(
                    PlaneType(
                        id=self.plane_type_records[-1].id + 1
                        if len(self.plane_type_records) > 0
                        else 1,
                        type=model,
                        iata=iata
                    ))
                if iata != "" \
                        and iata != "\\N" \
                        and iata != "-" \
                        and iata != "N/A" \
                        and any(
                            model in plane_name
                            for plane_name, *_
                            in CrossReferencesBuffer.plane_name.items()
                                ):
                    CrossReferencesBuffer.plane_type_iata[iata] = []
                    for plane_name, plane_id, *_ in CrossReferencesBuffer.plane_name.items():
                        # Add iata in the temporary list, to facilitate cross-referencing
                        if model in plane_name:
                            CrossReferencesBuffer.plane_type_iata[iata].append(plane_id)

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
    def records_lists(self) -> Dict[str, List]:
        """Get all records per type
        :return: a dict of all records per name
        """
        return {
            'Airlines': self.airway_records,
            'Airports': self.airport_records,
            'Airways': self.airway_records,
            'Cities': self.city_records,
            'Countries': self.country_records,
            'DSTs': self.dst_records,
            'Fly On': self.fly_on_records,
            'Planes': self.plane_records,
            'Plane Types': self.plane_type_records,
            'Steps': self.step_in_records,
            'Timezones': self.timezone_records,
            'Uses': self.use_records
        }

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
