from dataclasses import dataclass


@dataclass
class Airline:
    alias: str
    callsign: str
    iata: str
    icao: str
    id: int
    id_country: int
    is_active: bool
    name: str


@dataclass
class Airway:
    codeshare: str
    id: int
    stops: int


@dataclass
class City:
    id: int
    id_country: int
    id_timezone: int
    name: str
    population: int


@dataclass
class Country:
    area: float
    id: int
    id_dst: int
    name: str
    population: int


@dataclass
class Dst:
    id: int
    name: str


@dataclass
class FlyOn:
    id_airway: int
    id_plane: int


@dataclass
class Plane:
    capacity: int
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
    id: int
    type: str
    iata: str


@dataclass
class StepIn:
    id_airway: int
    id_airport: int
    rank: int


@dataclass
class Timezone:
    id: int
    name: str
    padding: int


@dataclass
class Use:
    id_airline: int
    id_airway: int
