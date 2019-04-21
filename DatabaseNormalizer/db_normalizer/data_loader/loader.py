# -*- coding: utf-8 -*-
"""
    db_normalizer.data_loader.loader
    -------------------------------

    Extract and store data contained in the .csv files.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
from typing import List, Dict

from db_normalizer.csv_handler.reader import Reader
from db_normalizer.csv_handler.utils import Csv
from db_normalizer.data_loader.utils.table_objects \
    import Airline, Timezone, Use, Airway, City, Country, Dst, FlyOn, \
    Plane, PlaneType, StepIn, NOT_SET, Airport
from db_normalizer.data_loader.utils.utils import Sources


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
            'airlines': Reader(Sources.airlines),
            'airports': Reader(Sources.airports),
            'flight_numbers': Reader(Sources.flight_numbers),
            'planes': Reader(Sources.planes),
            'routes': Reader(Sources.routes),
        }

    def load_all(self):
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

        # linking table
        self.load_step_in_use()
        self.load_fly_on()

    def load_step_in_use(self):
        """Link airway and airport table
        """
        airwayID = 0
        # Création d'une liste temporaire pour sauvegarder les chemins créent (step1-step2...)
        path = []
        # Création d'une liste temporaire pour sauvegarder les chemins associer au airline (airline, step1-step2...)
        airlinePath = []
        # Remplissage depuis le fichier flight_numbers
        for airline, _, airportIcao \
                in self._reader['flight_numbers'].read_content(skip_header=True):

            # On retrouve l'id de l'airline
            for airl in self.airline_records:
                if airline == airl.icao:
                    airlineID = airl.id
            airlinePath.append(airlineID, airportIcao)
            self.use_records(
                Use(
                    id_airline=airlineID,
                    id_airway=airwayID
                )
            )

            # Si le chemin n'est pas connue
            if airportIcao not in path:
                path.append(airportIcao)
                # initialisation du rang
                r = 0
                # Pour chaque icao d'aeroport
                for icao in airportIcao.split('-'):
                    for airport in self.airport_records:
                        # On match l'icao du fichier avec celui de airport pour retrouver l'id
                        if airport.icao == icao:
                            self.step_in_records(
                                StepIn(
                                    id_airport=airport.id,
                                    id_airway=airwayID,
                                    rank=r
                                )
                            )
                    r = r + 1
                airwayID = airwayID + 1

        # Remplissage depuis le fichier routes
        for airline, _, airportSrc, _, airportDest, _, _, stops, *_ \
                in self._reader['routes'].read_content(skip_header=False):

            # On retrouve l'id de l'airline
            for airl in self.airline_records:
                if airline == airl.icao or airline == airl.iata:
                    airlineID = airl.id

            # On retrouve l'id de l'aeroport source et destination
            for airport in self.airport_records:
                if airportSrc == airport.iata or airportSrc == airport.icao:
                    airpS = airport.id
                    airpSIcao = airport.icao
                if airportDest == airport.iata or airportDest == airport.icao:
                    airpD = airport.id
                    airpDIcao = airport.icao

            # On cherche si l'utilisation du chemin par cette airline est déjà connue
            # (possibilité d'utiliser un not in ?)
            notExist = True
            for airlID, path in airlinePath:
                step = path.split('-')
                if airlineID == airlID and step[0] == airpSIcao and step(len(step) - 1) == airpDIcao \
                    and len(step) == stops + 2:
                    notExist = False

            if notExist:
                self.use_records(
                    Use(
                        id_airline=airlineID,
                        id_airway=airwayID
                    )
                )

            # On cherche si le chemin est déjà connue (possibilité d'utiliser un not in ?)
            notExist = True
            for path in path:
                step = path.split('-')
                if step[0] == airpSIcao and step[len(step) - 1] == airpDIcao and len(step) == stops + 2:
                    notExist = False

            if notExist:
                self.step_in_records(
                    StepIn(
                        id_airport=airpS,
                        id_airway=airwayID,
                        rank=0
                    )
                )
                self.step_in_records(
                    StepIn(
                        id_airport=airpD,
                        id_airway=airwayID,
                        rank=1
                    )
                )
                airwayID = airwayID + 1

    def load_fly_on(self):
        """Link airway and plane table
        """
        for _, _, airportSrc, _, airportDest, _, _, stops, equipement \
                in self._reader['routes'].read_content(skip_header=False):

            # On retrouve l'id de l'aeroport source et destination
            for airport in self.airport_records:
                if airportSrc == airport.iata or airportSrc == airport.icao:
                    airpS = airport.id
                if airportDest == airport.iata or airportDest == airport.icao:
                    airpD = airport.id

            for airway in self.airway_records:
                for step0 in self.step_in_records:
                    if airway.id == step0.id_airway:
                        if step0.id_airport == airpS and step0.rank == 0:
                            for stepEnd in self.step_in_records:
                                if airway.id == stepEnd.id_airway:
                                    if stepEnd.id_airport == airpD and stepEnd.rank == stops + 1:
                                        for plane in equipement.split(' '):
                                            self.fly_on_records(
                                                FlyOn(
                                                    id_airway=airway.id,
                                                    id_plane=plane
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
            idCountry = NOT_SET
            for C in self.country_records:
                if country == C.name:
                    idCountry = C.id

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
                    id_country=idCountry,
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

        # timezones['name'] = padding
        timezones: Dict[str, int] = dict()

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
                        passenger=NOT_SET,
                        fret=NOT_SET,
                        speed=NOT_SET,
                        consumption=NOT_SET
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
