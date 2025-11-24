import dataclasses
from collections import namedtuple
from typing import List, Optional
from math import radians, sin, cos, sqrt, atan2

from geopy import Point


class Coordinate(namedtuple('Coordinate', ['latitude', 'longitude'])):

    def distance_to(self, other):
        """Calculate distance in miles using Haversine formula"""
        R = 3959
        lat1, lon1 = radians(self.latitude), radians(self.longitude)
        lat2, lon2 = radians(other.latitude), radians(other.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c

    def __str__(self):
        return f"{self.latitude},{self.longitude}"

    def as_tuple(self):
        return self.latitude, self.longitude


    def as_point(self):
        return Point(self.latitude, self.longitude)


@dataclasses.dataclass(frozen=True)
class SamplePoint:
    latitude: float
    longitude: float
    distance_from_start: float

    def as_coordinate(self):
        return Coordinate(self.latitude, self.longitude)


@dataclasses.dataclass(frozen=True)
class RouteData:
    coordinates: List[Coordinate]
    distance: float
    geometry: List
    duration: float = None
    start: Coordinate = None
    finish: Coordinate = None


@dataclasses.dataclass(frozen=True)
class OptimizedRouteResult:
    stops: List['FuelStation']
    cost: float
    gallons: float


@dataclasses.dataclass
class FuelStation:
    id: str
    name: str
    address: str
    city: str
    state: str
    price: float
    location: str
    coords: Coordinate
    distance_from_point: float
    distance_from_start: Optional[float] = None
    segment_index: Optional[int] = None
    gallons: Optional[float] = None
    cost: Optional[float] = None
    distance_from_route: Optional[float] = None
