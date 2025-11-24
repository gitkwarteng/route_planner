import hashlib
from typing import List, Dict, Optional
from django.core.cache import cache
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
# from django.contrib.gis.geos import GEOSGeometry
from geopy.distance import geodesic

from routing.models import FuelStation
from routing.data import Coordinate, FuelStop, SamplePoint


class StationService:

    @staticmethod
    def get_sample_points_along_route(
            with_coordinates: List[Coordinate],
            at_intervals: float = 100
    ) -> List[SamplePoint]:
        """
        Get sample points along the route at regular intervals.
        :param with_coordinates: The list of coordinates from the route
        :param at_intervals: The interval in miles to locate sample points. Default is 100.
        :return Returns list of SamplePoints.
        """
        points = []
        cumulative_distance = 0
        last_sample_distance = 0

        # Add starting point
        points.append(
            SamplePoint(
                latitude=with_coordinates[0].latitude,
                longitude=with_coordinates[0].longitude,
                distance_from_start=0
            )
        )

        for i in range(1, len(with_coordinates)):
            prev = with_coordinates[i - 1]
            curr = with_coordinates[i]

            # Calculate segment distance
            segment_dist = geodesic(
                prev.as_tuple(), curr.as_tuple()
            ).miles
            cumulative_distance += segment_dist

            # Check if we should add a sample point
            while cumulative_distance - last_sample_distance >= at_intervals:
                last_sample_distance += at_intervals
                # Interpolate position
                ratio = (last_sample_distance - (cumulative_distance - segment_dist)) / segment_dist
                lat = prev.latitude + ratio * (curr.latitude - prev.latitude)
                lon = prev.longitude + ratio * (curr.longitude - prev.longitude)

                points.append(SamplePoint(
                    latitude=lat, longitude=lon,
                    distance_from_start=last_sample_distance
                ))

        # Add ending point
        points.append(SamplePoint(
            latitude=with_coordinates[-1][1],
            longitude=with_coordinates[-1][0],
            distance_from_start=cumulative_distance
        ))

        return points


    @staticmethod
    def find_nearby_stops_for_point(*, lat: float, lon: float, max_distance: float = 25) -> List[FuelStop]:
        """Find truck stops within radius of a point."""
        cache_key = f"stops:{hashlib.md5(f'{lat},{lon},{max_distance}'.encode()).hexdigest()}"
        cached = cache.get(cache_key)
        if cached:
            return [FuelStop(**s) for s in cached]

        nearby = []
        ref_point = Point(lon, lat)

        stations = FuelStation.objects.filter(
            location__distance_lte=(ref_point, D(mi=max_distance))
        ).annotate(
            distance=Distance('location', ref_point)
        ).order_by('price')[:20]

        for station in stations:
            nearby.append(FuelStop(
                id=station.opis_id,
                name=station.name,
                address=station.address,
                city=station.city,
                state=station.state,
                price=float(station.price),
                location=f"{station.city}, {station.state}, USA",
                latitude=station.location.y,
                longitude=station.location.x,
                distance_from_point=station.distance.mi
            ))

        result = sorted(nearby, key=lambda x: x.price)
        cache.set(cache_key, [s.as_dict for s in result], timeout=3600)
        return result

    @staticmethod
    def index_stops_by_segment_for_route(with_points: List[SamplePoint]) -> Dict[int, List[FuelStop]]:
        """Pre-compute stops near each route segment for efficiency."""
        stops_by_segment = {}

        for i, p in enumerate(with_points):
            nearby = StationService.find_nearby_stops_for_point(lat=p.latitude, lon=p.longitude)
            for stop in nearby:
                stop.distance_from_start = p.distance_from_start
                stop.segment_index = i
            stops_by_segment[i] = nearby

        return stops_by_segment


    @staticmethod
    def find_best_stop_in_range(
        *,
        stops_by_segment: Dict[int, List[FuelStop]],
        start_distance: float,
        max_distance: float,
        total_distance: float
    ) -> Optional[FuelStop]:
        """Find the cheapest stop within the driveable range."""
        candidates = []

        for seg_idx, stops in stops_by_segment.items():
            for stop in stops:
                route_dist = stop.distance_from_start
                if start_distance < route_dist <= min(max_distance, total_distance):
                    candidates.append(stop)

        if not candidates:
            return None

        # Return cheapest option
        return min(candidates, key=lambda x: x.price)
