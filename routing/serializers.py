from rest_framework import serializers

class RouteRequestSerializer(serializers.Serializer):
    start = serializers.CharField(required=True)
    finish = serializers.CharField(required=True)


class FuelStopSerializer(serializers.Serializer):
    name = serializers.CharField()
    address = serializers.CharField()
    location = serializers.CharField()
    price = serializers.FloatField()
    gallons = serializers.FloatField()
    cost = serializers.FloatField()
    distance_from_start = serializers.FloatField()
    distance_from_route = serializers.FloatField()


class RouteResponseSerializer(serializers.Serializer):
    route = serializers.ListField()
    total_distance = serializers.FloatField()
    stops = FuelStopSerializer(many=True)
    total_cost = serializers.FloatField()
    total_gallons = serializers.FloatField()
    map = serializers.CharField(required=False)
    message = serializers.CharField(required=False)
