#spotterapi/routes/services/routing_service.py
import requests
from geopy.distance import geodesic
import pandas as pd
from django.conf import settings

class RoutingService:
    @staticmethod
    def get_route(start, end):
        url = f"https://api.tomtom.com/routing/1/calculateRoute/{start}:{end}/json"
        params = {
            "key": settings.TOMTOM_API_KEY,
            "routeType": "fastest",
            "travelMode": "car",
            "traffic": "false",
        }
        response = requests.get(url, params=params)
        data = response.json()
        if "routes" not in data:
            raise Exception("No route found!")
        points = data["routes"][0]["legs"][0]["points"]
        route = [(pt["latitude"], pt["longitude"]) for pt in points]
        distance = data["routes"][0]["summary"]["lengthInMeters"] / 1609.34  # in miles
        return route, distance

    @staticmethod
    def get_segment_points(route, segment_length):
        segment_points = []
        total_distance = 0
        last_point = route[0]
        for point in route[1:]:
            dist = geodesic(last_point, point).miles
            total_distance += dist
            if total_distance >= segment_length:
                segment_points.append(point)
                total_distance = 0
            last_point = point
        return segment_points

    @staticmethod
    def compute_total_cost(distance, stops, mpg):
        gallons = distance / mpg
        avg_price = sum([stop["price"] for stop in stops]) / len(stops) if stops else 0
        return round(gallons * avg_price, 2)
    @staticmethod
    def is_in_usa(lat, lon):
        """Check if coordinates are within USA bounding box"""
        min_lat, max_lat = 24.396308, 49.384358
        min_lon, max_lon = -125.000000, -66.934570
        return (min_lat <= lat <= max_lat) and (min_lon <= lon <= max_lon)

    @staticmethod
    def validate_us_coordinates(start, end):
        """Validate both start and end are in USA"""
        try:
            start_lat, start_lon = map(float, start.split(','))
            end_lat, end_lon = map(float, end.split(','))
            
            if not (RoutingService.is_in_usa(start_lat, start_lon) and 
                    RoutingService.is_in_usa(end_lat, end_lon)):
                raise ValueError("Your start and end points aren't in USA")
            return True
        except ValueError as e:
            raise ValueError("Invalid coordinate format or location outside USA")
