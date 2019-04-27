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
global path, airline_path

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
        # group loading
        self.load_geographical_data()
        self.load_plane_data()

        # table with references to others
        self.load_airline()

        # linking table
        self.load_airway_details()
        self.load_fly_on()

    def load_airway_details(self):
        """Link airway and airport table
        """
        # Création d'une liste temporaire pour sauvegarder les chemins créent (step1-step2...)
        path = []
        # Création d'une liste temporaire pour sauvegarder les chemins associer au airline (airline, step1-step2...)
        airline_path = []
        # Remplissage depuis le fichier flight_numbers
        for airline_code, _, airport_icao \
                in self._reader['flight_numbers'].read_content(skip_header=True):

            if airport_icao in path:
                # On retrouve l'index du chemin dans path depuis lequel on peut facillment retourver l'id de l'airway
                # (index + 1, car l'id commence à 1)
                airway_id = path.index(airport_icao) + 1
            else:
                # On ajoute le nouveau chemin
                path.append(airport_icao)
                if len(self.airway_records) > 0:
                    airway_id = self.airway_records[-1].id + 1
                else:
                    airway_id = 1
                # On crée une nouvelle airway correspondant à ce chemin
                self.airway_records.append(
                    Airway(
                        id=airway_id,
                        codeshare=NOT_SET
                    )
                )

                # initialisation du rang
                rank = 0
                # Pour chaque icao d'aeroport, on récupère les aeroport séparé par "-" (step1-step2...)
                for icao_stop in airport_icao.split('-'):
                    for airport in self.airport_records:
                        # On match l'icao du fichier avec celui de airport pour retrouver l'id
                        if airport.icao == icao_stop:
                            self.step_in_records.append(
                                StepIn(
                                    id_airport=airport.id,
                                    id_airway=airway_id,
                                    rank=rank
                                )
                            )
                            # On arrete lorsque on trouve l'aeroport
                            break
                    rank += 1

            # On retrouve l'id de l'airline
            for airline in self.airline_records:
                if airline_code == airline.icao:
                    # On enregistre le chemain associer à l'airline pour la recherche dans le second fichier
                    airline_path.append([airline.id, airport_icao])
                    self.use_records.append(
                        Use(
                            id_airline=airline.id,
                            id_airway=airway_id
                        )
                    )
                    # On arrete lorsque on trouve l'airline
                    break

        # Remplissage depuis le fichier routes
        for airline_code, _, airport_src, _, airport_dest, _, codeshare, stops, *_ \
                in self._reader['routes'].read_content(skip_header=False):

            airp_src_icao = "unknown"
            airp_dest_icao = "unknown"
            airp_src = 0
            airp_dest = 0

            airway_id = self.airway_records[-1].id + 1
            # On retrouve l'id et l'icao des l'aeroports source et destination
            for airport in self.airport_records:
                if airport_src == airport.iata \
                        or airport_src == airport.icao:
                    airp_src = airport.id
                    airp_src_icao = airport.icao
                    # On arrete lorsque on trouve l'aeroport
                    break

                if airport_dest == airport.iata \
                        or airport_dest == airport.icao:
                    airp_dest = airport.id
                    airp_dest_icao = airport.icao
                    # On arrete lorsque on trouve l'aeroport
                    break

            # On cherche si le chemin est déjà connue (possibilité d'utiliser un not in ?)
            exist = False
            i = 1
            for airway in path:
                step = airway.split('-')
                if step[0] == airp_src_icao \
                        and step[-1] == airp_dest_icao \
                        and len(step) == stops + 2:
                    exist = True
                    # L'index + 1 du chemin dans path correspond à l'id de l'airway
                    airway_id = i
                    # On arrete si on trouve un chemin identique
                    break
                i += 1

            if not exist:
                # create an airway from the extracted data and add it to
                # the stored records

                # On ajoute le nouveau chemin
                path.append(airp_src_icao + "-" + airp_dest_icao)

                self.airway_records.append(
                    Airway(
                        id=airway_id,
                        codeshare=codeshare
                    )
                )
                self.step_in_records.append(
                    StepIn(
                        id_airport=airp_src,
                        id_airway=airway_id,
                        rank=0
                    )
                )
                self.step_in_records.append(
                    StepIn(
                        id_airport=airp_dest,
                        id_airway=airway_id,
                        rank=1
                    )
                )

            # On retrouve l'id de l'airline
            for airline in self.airline_records:
                if airline_code == airline.icao \
                        or airline_code == airline.iata:
                    airline_id = airline.id
                    # On arrete lorsque on trouve l'airline
                    break

            # On cherche si l'utilisation du chemin par cette airline est déjà connue
            # (possibilité d'utiliser un not in ?)
            exist = False
            for airl_id, airway in airline_path:
                step = airway.split('-')
                if airline_id == airl_id \
                        and step[0] == airp_src_icao \
                        and step[-1] == airp_dest_icao \
                        and len(step) == stops + 2:
                    exist = True
                    # On arrete si on trouve le chemin indentique associer à cette airline
                    break

            if not exist:
                airline_path.append([airline_id, airp_src_icao + "-" + airp_dest_icao])
                self.use_records.append(
                    Use(
                        id_airline=airline_id,
                        id_airway=airway_id
                    )
                )

    def load_fly_on(self):
        """Link airway and plane table
        """
        for _, _, airport_src, _, airport_dest, _, _, stops, equipement \
                in self._reader['routes'].read_content(skip_header=False):

            # On retrouve l'id de l'aeroport source et destination
            for airport in self.airport_records:
                if airport_src == airport.iata or airport_src == airport.icao:
                    airp_src = airport.id
                if airport_dest == airport.iata or airport_dest == airport.icao:
                    airp_dest = airport.id

            for airway in self.airway_records:
                for step0 in self.step_in_records:
                    if airway.id == step0.id_airway:
                        if step0.id_airport == airp_src and step0.rank == 0:
                            for stepEnd in self.step_in_records:
                                if airway.id == stepEnd.id_airway:
                                    if stepEnd.id_airport == airp_dest and stepEnd.rank == stops + 1:
                                        for plane in equipement.split(' '):
                                            self.fly_on_records.append(
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
            id_country = NOT_SET
            for country_list in self.country_records:
                if country == country_list.name:
                    id_country = country_list.id

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
