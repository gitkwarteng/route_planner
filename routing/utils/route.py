from typing import List
from routing.data import FuelStop, RouteData
from routing.utils.map import generate_map_url, generate_map_html


def make_response(*, route:RouteData, fuel_stops:List[FuelStop], total_cost:float, total_gallons:float, message=None):
    """Create a response dictionary for the API."""
    return {
        'total_distance': route.distance,
        'stops': [stop.as_dict for stop in fuel_stops],
        'total_cost': total_cost,
        'total_gallons': total_gallons,
        'map_url': generate_map_url(start=route.start, end=route.finish, stops=fuel_stops),
        'map': generate_map_html(route=route, stops=fuel_stops),
        # 'route': route.geometry,
        'message': message
    }