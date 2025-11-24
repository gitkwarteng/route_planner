from typing import Optional

from common.client import BaseRequestClient
from .data import Coordinate, RouteData


class RoutingClient(BaseRequestClient):

    base_url = 'https://router.project-osrm.org/route/v1/'


    def get_route(self, *, from_location: Coordinate, to_location: Coordinate) -> Optional[RouteData]:
        """
        Get route data for specified locations.
        :param from_location: The location route is starting from.
        :param to_location: The finish location for route.
        :return: Returns a route data if route was found, else None.
        """
        coords = f"{from_location.__str__()};{to_location.__str__()}"

        endpoint = f'driving/{coords}'

        params = {
            'overview': 'full',
            'geometries': 'geojson',
            'steps': 'false'
        }

        response = self.get(endpoint, params=params)

        if response.get('code') == 'Ok' and response.get('routes'):
            route = response['routes'][0]
            return RouteData(
                distance=route['distance'] / 1609.34,  # Convert to miles
                duration=route['duration'] / 60,  # Convert to minutes
                geometry=route['geometry'],
                coordinates=[Coordinate(latitude=lat, longitude=lon) for lon, lat in route['geometry']['coordinates']],
                start=from_location,
                finish=to_location
            )

        return None
