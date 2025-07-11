#spotterapi/routes/serializers.py
from rest_framework import serializers

class RouteRequestSerializer(serializers.Serializer):
    start= serializers.CharField(required=True)
    end= serializers.CharField(required=True)


class FuelStopSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.FloatField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()

class RouteResponseSerializer(serializers.Serializer):
    total_distance = serializers.FloatField()
    total_cost = serializers.FloatField()
    fuel_stops = FuelStopSerializer(many=True)
    map_html = serializers.CharField()