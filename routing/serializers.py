from rest_framework import serializers

from routing.utils.validation import is_valid_us_address


class RouteRequestSerializer(serializers.Serializer):
    start = serializers.CharField(required=True, help_text='Starting location (e.g., "Los Angeles, CA")')
    finish = serializers.CharField(required=True, help_text='Ending location (e.g., "San Francisco, CA")')
    
    def validate_start(self, value):
        if not is_valid_us_address(value):
            raise serializers.ValidationError("Address must be in format 'City, State' or 'City, State, USA' within the United States")
        return value
    
    def validate_finish(self, value):
        if not is_valid_us_address(value):
            raise serializers.ValidationError("Address must be in format 'City, State' or 'City, State, USA' within the United States")
        return value



class FuelStopSerializer(serializers.Serializer):
    name = serializers.CharField()
    address = serializers.CharField()
    location = serializers.CharField()
    price = serializers.FloatField()
    gallons = serializers.FloatField()
    cost = serializers.FloatField()
    distance_from_start = serializers.FloatField()
    distance_from_point = serializers.FloatField()


class RouteResponseSerializer(serializers.Serializer):
    route = serializers.ListField()
    total_distance = serializers.FloatField()
    stops = FuelStopSerializer(many=True)
    total_cost = serializers.FloatField()
    total_gallons = serializers.FloatField()
    map = serializers.CharField(required=False)
    message = serializers.CharField(required=False)
