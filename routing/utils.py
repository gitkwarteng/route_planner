from typing import List

from routing.types import Coordinate, FuelStation, RouteData


def generate_map_url(start:Coordinate, end:Coordinate, fuel_stops:List[FuelStation]):
    """Generate a URL to view the route on OpenStreetMap."""
    # Create markers string for uMap or similar
    markers = [str(start)]

    for stop in fuel_stops:
        markers.append(f"{stop.coords.latitude},{stop.coords.longitude}")
    markers.append(str(end))

    # Basic OSM link showing the route bounds
    min_lat = min(start.latitude, end.latitude, *[s.coords.latitude for s in fuel_stops]) if fuel_stops else min(start.latitude, end.latitude)
    max_lat = max(start.latitude, end.latitude, *[s.coords.latitude for s in fuel_stops]) if fuel_stops else max(start.latitude, end.latitude)
    min_lon = min(start.longitude, end.longitude, *[s.coords.longitude for s in fuel_stops]) if fuel_stops else min(start.longitude, end.longitude)
    max_lon = max(start.longitude, end.longitude, *[s.coords.longitude for s in fuel_stops]) if fuel_stops else max(start.longitude, end.longitude)

    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    return f"https://www.openstreetmap.org/?mlat={center_lat}&mlon={center_lon}#map=6/{center_lat}/{center_lon}"


def make_response(*, route:RouteData, fuel_stops:List[FuelStation], total_cost:float, total_gallons:float, message=None):
    """Create a response dictionary for the API."""
    return {
        'route': route.geometry,
        'total_distance': route.distance,
        'stops': fuel_stops,
        'total_cost': total_cost,
        'total_gallons': total_gallons,
        'map': generate_map_url(route.start, route.finish, fuel_stops),
        'message': message
    }