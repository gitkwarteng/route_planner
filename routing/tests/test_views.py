from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock


class RouteViewSetTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def test_list_endpoint(self):
        response = self.client.get('/api/route/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('endpoints', response.data)
    
    def test_plan_missing_parameters(self):
        response = self.client.get('/api/route/plan/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_plan_invalid_address_format(self):
        response = self.client.get('/api/route/plan/?start=InvalidAddress&finish=Phoenix, AZ')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @patch('routing.services.geolocation.GeoLocationService.geocode')
    @patch('routing.client.RoutingClient.get_route')
    def test_plan_valid_request(self, mock_route, mock_geocode):
        from routing.data import Coordinate, RouteData
        
        mock_geocode.return_value = Coordinate(latitude=34.05, longitude=-118.25)
        mock_route.return_value = RouteData(
            distance=100,
            duration=120,
            coordinates=[Coordinate(34.05, -118.25), Coordinate(33.45, -112.07)],
            start=Coordinate(34.05, -118.25),
            finish=Coordinate(33.45, -112.07)
        )
        
        response = self.client.get('/api/route/plan/?start=Los Angeles, CA&finish=Phoenix, AZ')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
