"""TODO
"""
from dataclasses import dataclass


"""TODO"""
NOT_SET = -1


@dataclass
class Airline:
    """TODO
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
    """TODO
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
    """TODO
    """
    codeshare: str
    id: int


@dataclass
class City:
    """TODO
    """
    id: int
    id_country: int
    id_timezone: int
    name: str
    population: int


@dataclass
class Country:
    """TODO
    """
    area: float
    id: int
    id_dst: int
    name: str
    population: int


@dataclass(frozen=True)
class Dst:
    """TODO
    """
    id: int
    name: str


@dataclass
class FlyOn:
    """TODO
    """
    id_airway: int
    id_plane: int


@dataclass
class Plane:
    """TODO
    """
    passenger: int
    consumption: float
    fret: float
    iata: str
    icao: str
    id: int
    id_plane_type: int
    model: str
    speed: int


@dataclass
class PlaneType:
    """TODO
    """
    id: int
    type: str
    iata: str


@dataclass
class StepIn:
    """TODO
    """
    id_airway: int
    id_airport: int
    rank: int


@dataclass(frozen=True)
class Timezone:
    """TODO
    """
    id: int
    name: str
    padding: float


@dataclass
class Use:
    """TODO
    """
    id_airline: int
    id_airway: int
