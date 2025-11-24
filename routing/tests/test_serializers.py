from django.test import TestCase
from routing.serializers import RouteRequestSerializer


class RouteRequestSerializerTest(TestCase):
    
    def test_valid_us_addresses(self):
        data = {'start': 'Los Angeles, CA', 'finish': 'Phoenix, AZ'}
        serializer = RouteRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_valid_us_addresses_with_usa(self):
        data = {'start': 'New York, NY, USA', 'finish': 'Boston, MA, USA'}
        serializer = RouteRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_invalid_state_code(self):
        data = {'start': 'Los Angeles, XX', 'finish': 'Phoenix, AZ'}
        serializer = RouteRequestSerializer(data=data)
        self.assertFalse(serializer.is_valid())
    
    def test_missing_state(self):
        data = {'start': 'Los Angeles', 'finish': 'Phoenix, AZ'}
        serializer = RouteRequestSerializer(data=data)
        self.assertFalse(serializer.is_valid())
    
    def test_non_us_country(self):
        data = {'start': 'Toronto, ON, Canada', 'finish': 'Phoenix, AZ'}
        serializer = RouteRequestSerializer(data=data)
        self.assertFalse(serializer.is_valid())
