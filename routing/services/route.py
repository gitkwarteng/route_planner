import logging
from typing import List, Dict

from .station import StationService
from routing.types import SamplePoint, FuelStation, OptimizedRouteResult

logger = logging.getLogger('routing.route')


class RouteService:

    def __init__(
            self, *,
            vehicle_range: float = 500,
            mpg: float = 10,
            search_radius: float = 25  # Miles off route to search
    ):
        self.vehicle_range = vehicle_range
        self.mpg = mpg
        self.tank_capacity = vehicle_range / mpg
        self.search_radius = search_radius
        self.reserve_miles = 50  # Safety reserve


    def get_optimized_stops_for_route(
            self, *,
            with_points: List[SamplePoint],
            total_distance: float,
            current_fuel_level: float = 1
    ) -> OptimizedRouteResult:
        """
        Find optimal fuel stops along the route.

        Args:
            with_points: List of SamplePoints along route
            total_distance: Total route distance in miles
            current_fuel_level: Starting fuel as fraction of tank (0-1)

        Returns:
            List of recommended FuelStop objects
        """
        logger.info(f"Optimizing fuel stops for {total_distance} mile route")
        stops = []
        total_gallons = 0
        total_cost = 0

        current_miles = current_fuel_level * self.tank_capacity * self.mpg
        distance_traveled = 0

        # Build index of stops near each route point
        stops_by_segment = StationService.index_stops_by_segment_for_route(with_points=with_points)

        while distance_traveled < total_distance:
            # Calculate when we need to refuel
            safe_range = current_miles - self.reserve_miles
            must_fuel_by = distance_traveled + safe_range

            if must_fuel_by >= total_distance:
                # Can reach destination without refueling
                break

            # Find best stop before we must refuel
            best_stop = StationService.find_best_stop_in_range(
                stops_by_segment=stops_by_segment,
                start_distance=distance_traveled,
                max_distance=must_fuel_by,
                total_distance=total_distance
            )

            if best_stop is None:
                logger.warning(f"No fuel stop found at distance {distance_traveled}")
                break

            # Calculate how much fuel to buy
            stop_distance = best_stop.distance_from_start
            miles_used = stop_distance - distance_traveled
            current_miles -= miles_used

            # Look ahead for cheaper options
            gallons_needed = self._calculate_optimal_gallons(
                current_stop=best_stop,
                stops_by_segment=stops_by_segment,
                current_distance=stop_distance,
                current_fuel_miles=current_miles,
                total_distance=total_distance
            )

            best_stop.gallons=round(gallons_needed, 2)
            best_stop.cost=round(gallons_needed * best_stop.price, 2)

            total_gallons += gallons_needed
            total_cost += best_stop.cost


            stops.append(best_stop)
            logger.debug(f"Added stop at {stop_distance} miles: {best_stop.name}, ${best_stop.cost}")

            # Update state
            current_miles += gallons_needed * self.mpg
            distance_traveled = stop_distance

        logger.info(f"Optimized route: {len(stops)} stops, ${round(total_cost, 2)} total cost")
        return OptimizedRouteResult(stops=stops, cost=total_cost, gallons=total_gallons)


    def _calculate_optimal_gallons(
            self, *,
            current_stop: FuelStation,
            stops_by_segment: Dict[int, List[FuelStation]],
            current_distance: float,
            current_fuel_miles: float,
            total_distance: float
    ) -> float:
        """
        Calculate optimal gallons to purchase at current stop.
        Uses look-ahead to find if cheaper options exist ahead.
        """
        current_price = current_stop.price
        max_range = self.tank_capacity * self.mpg

        # Look ahead for cheaper stops
        cheaper_stop_distance = None
        look_ahead_range = current_distance + max_range

        for seg_idx, stops in stops_by_segment.items():
            for stop in stops:
                route_dist = stop.distance_from_start
                if current_distance < route_dist <= look_ahead_range:
                    if stop.price < current_price * 0.95:  # 5% cheaper threshold
                        if cheaper_stop_distance is None or route_dist < cheaper_stop_distance:
                            cheaper_stop_distance = route_dist

        # Calculate gallons needed
        remaining_distance = total_distance - current_distance

        if cheaper_stop_distance is not None:
            # Only buy enough to reach cheaper stop (plus reserve)
            miles_to_cheaper = cheaper_stop_distance - current_distance
            miles_needed = miles_to_cheaper + self.reserve_miles - current_fuel_miles
            gallons = max(0, miles_needed / self.mpg)
        else:
            # No cheaper stop ahead - fill up more
            # Buy enough for remaining trip or fill tank
            miles_needed = min(remaining_distance + self.reserve_miles, max_range) - current_fuel_miles
            gallons = max(0, miles_needed / self.mpg)

        # Ensure we don't exceed tank capacity
        current_gallons = current_fuel_miles / self.mpg
        max_gallons = self.tank_capacity - current_gallons
        gallons = min(gallons, max_gallons)

        # Minimum purchase of 5 gallons if stopping
        return max(5, gallons)


    # def plan_fuel_stops(self, *, start:str, end:str, max_range=500, mpg=10):
    #     route_data = self.get_route(start, end)
    #     route_coords = route_data.coordinates
    #     total_distance = route_data.distance
    #
    #     nearby_stations = StationService.find_nearby_stations_for_route(route_coords)
    #
    #     if not nearby_stations:
    #         return {
    #             'route': route_data.geometry,
    #             'total_distance': total_distance,
    #             'fuel_stops': [],
    #             'total_fuel_cost': 0,
    #             'message': 'No fuel stations found near route'
    #         }
    #
    #     fuel_stops = []
    #     current_distance = 0
    #     remaining_range = max_range
    #     total_cost = 0
    #
    #     while current_distance + remaining_range < total_distance:
    #         target_distance = current_distance + max_range * 0.9
    #
    #         best_station = None
    #         best_score = float('inf')
    #
    #         for station in nearby_stations:
    #             station_distance = self._estimate_station_distance(
    #                 route_coords, station.coords, current_distance, total_distance
    #             )
    #
    #             if current_distance < station_distance <= target_distance:
    #                 score = station['price'] + station['distance_from_route'] * 0.1
    #                 if score < best_score:
    #                     best_score = score
    #                     best_station = station
    #                     best_station['route_distance'] = station_distance
    #
    #         if not best_station:
    #             best_station = nearby_stations[0]
    #             best_station['route_distance'] = target_distance
    #
    #         distance_traveled = best_station['route_distance'] - current_distance
    #         gallons_needed = distance_traveled / mpg
    #         cost = gallons_needed * best_station['price']
    #
    #         fuel_stops.append({
    #             'name': best_station['name'],
    #             'address': best_station['address'],
    #             'location': best_station['location'],
    #             'price_per_gallon': round(best_station['price'], 2),
    #             'gallons': round(gallons_needed, 2),
    #             'cost': round(cost, 2),
    #             'distance_from_start': round(best_station['route_distance'], 2)
    #         })
    #
    #         total_cost += cost
    #         current_distance = best_station['route_distance']
    #         remaining_range = max_range
    #
    #     final_distance = total_distance - current_distance
    #     final_gallons = final_distance / mpg
    #     if nearby_stations:
    #         final_cost = final_gallons * nearby_stations[0]['price']
    #         total_cost += final_cost
    #
    #     return {
    #         'route': route_data.geometry,
    #         'total_distance': round(total_distance, 2),
    #         'fuel_stops': fuel_stops,
    #         'total_fuel_cost': round(total_cost, 2),
    #         'total_gallons': round(total_distance / mpg, 2)
    #     }
    #
    # def _estimate_station_distance(self, route_coords, station_coords, start_dist, total_dist):
    #     min_idx = 0
    #     min_dist = float('inf')
    #
    #     for i, coord in enumerate(route_coords):
    #         dist = geodesic(coord, station_coords).miles
    #         if dist < min_dist:
    #             min_dist = dist
    #             min_idx = i
    #
    #     return (min_idx / len(route_coords)) * total_dist
