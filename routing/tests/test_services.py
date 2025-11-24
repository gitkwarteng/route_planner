from django.test import TestCase
from routing.data import Coordinate, SamplePoint
from routing.services.station import StationService


class StationServiceTest(TestCase):
    
    def test_get_sample_points_along_route(self):
        coordinates = [
            Coordinate(latitude=34.05, longitude=-118.25),
            Coordinate(latitude=34.10, longitude=-118.20),
            Coordinate(latitude=34.15, longitude=-118.15),
        ]
        
        points = StationService.get_sample_points_along_route(
            with_coordinates=coordinates,
            at_intervals=10
        )
        
        self.assertIsInstance(points, list)
        self.assertGreater(len(points), 0)
        self.assertIsInstance(points[0], SamplePoint)
        self.assertEqual(points[0].distance_from_start, 0)
    
    def test_sample_points_have_increasing_distance(self):
        coordinates = [
            Coordinate(latitude=34.0, longitude=-118.0),
            Coordinate(latitude=35.0, longitude=-118.0),
        ]
        
        points = StationService.get_sample_points_along_route(
            with_coordinates=coordinates,
            at_intervals=20
        )
        
        for i in range(1, len(points)):
            self.assertGreaterEqual(
                points[i].distance_from_start,
                points[i-1].distance_from_start
            )
