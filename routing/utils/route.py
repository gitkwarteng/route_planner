from typing import List
from routing.data import Coordinate, FuelStop, RouteData


def generate_map_url(*, start:Coordinate, end:Coordinate, stops:List[FuelStop]) -> str:
    """
    Generate map url for the given start and end location with stops.
    Args:
        start: The start location
        end: The end location
        stops: List of fuel stops

    Returns:
        URL string
    """
    # Create markers string for uMap or similar
    markers = [f"{start.latitude},{start.longitude}"]

    for stop in stops:
        markers.append(f"{stop.latitude},{stop.longitude}")

    markers.append(f"{end.latitude},{end.longitude}")

    # Basic OSM link showing the route bounds
    min_lat = min(start.latitude, end.latitude, *[s.latitude for s in stops]) if stops else min(start.latitude, end.latitude)
    max_lat = max(start.latitude, end.latitude, *[s.latitude for s in stops]) if stops else max(start.latitude, end.latitude)
    min_lon = min(start.longitude, end.longitude, *[s.longitude for s in stops]) if stops else min(start.longitude, end.longitude)
    max_lon = max(start.longitude, end.longitude, *[s.longitude for s in stops]) if stops else max(start.longitude, end.longitude)

    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    return f"https://www.openstreetmap.org/?mlat={center_lat}&mlon={center_lon}#map=6/{center_lat}/{center_lon}/size=600x400"


def make_response(*, route:RouteData, fuel_stops:List[FuelStop], total_cost:float, total_gallons:float, message=None):
    """Create a response dictionary for the API."""
    return {
        'total_distance': route.distance,
        'stops': [stop.as_dict for stop in fuel_stops],
        'total_cost': total_cost,
        'total_gallons': total_gallons,
        'map': generate_map_url(start=route.start, end=route.finish, stops=fuel_stops),
        # 'route': route.geometry,
        'message': message
    }