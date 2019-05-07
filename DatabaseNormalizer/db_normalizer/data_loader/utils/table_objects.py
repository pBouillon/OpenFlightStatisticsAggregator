# -*- coding: utf-8 -*-
"""
    db_normalizer.data_loader.table_objects
    ---------------------------------------

    Data structures to store normalized data.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
from dataclasses import dataclass


"""Default value for un-settable values"""
NOT_SET = -1

"""Default value for external data"""
EXTERNAL_DATA = -1


@dataclass
class Airline:
    """Airline table scheme
    """
    id: int
    id_country: int
    is_active: bool
    alias: str
    callsign: str
    name: str
    iata: str
    icao: str


@dataclass
class Airport:
    """Airport table scheme
    """
    id: int
    id_city: int
    altitude: float
    iata: str
    icao: str
    latitude: float
    longitude: float
    name: str


@dataclass(frozen=True)
class Airway:
    """Airway table scheme
    """
    id: int
    codeshare: str


@dataclass
class City:
    """City table scheme
    """
    id: int
    id_country: int
    id_timezone: int
    name: str
    population: int = EXTERNAL_DATA


@dataclass
class Country:
    """Country table scheme
    """
    id: int
    id_dst: int
    name: str
    area: float = EXTERNAL_DATA
    population: int = EXTERNAL_DATA


@dataclass(frozen=True)
class Dst:
    """Dst table scheme
    """
    id: int
    name: str


@dataclass
class FlyOn:
    """FlyOn table scheme
    """
    id_airway: int
    id_plane: int


@dataclass
class Plane:
    """Plane table scheme
    """
    id: int
    id_plane_type: int
    iata: str
    icao: str
    model: str
    passenger: int = EXTERNAL_DATA
    consumption: float = EXTERNAL_DATA
    fret: float = EXTERNAL_DATA
    speed: int = EXTERNAL_DATA


@dataclass(frozen=True)
class PlaneType:
    """PlaneType table scheme
    """
    id: int
    iata: str
    type: str


@dataclass
class StepIn:
    """StepIn table scheme
    """
    id: int
    id_airport: int
    id_airway: int
    rank: int


@dataclass(frozen=True)
class Timezone:
    """Timezone table scheme
    """
    id: int
    name: str
    padding: float


@dataclass
class Use:
    """Use table scheme
    """
    id_airline: int
    id_airway: int
