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
    alias: str
    callsign: str
    iata: str
    icao: str
    id: int
    id_country: int
    is_active: bool
    name: str


@dataclass
class Airport:
    """Airport table scheme
    """
    altitude: float
    iata: str
    icao: str
    id: int
    id_city: int
    latitude: float
    longitude: float
    name: str


@dataclass(frozen=True)
class Airway:
    """Airway table scheme
    """
    codeshare: str
    id: int


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
    iata: str
    icao: str
    id: int
    id_plane_type: int
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
    type: str
    iata: str


@dataclass
class StepIn:
    """StepIn table scheme
    """
    id_airway: int
    id_airport: int
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
