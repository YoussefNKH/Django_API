#spotterapi/routes/views.py
import base64
import tempfile
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from routes.services.fuel_service import FuelService
from routes.services.routing_service import RoutingService
from .serializers import RouteRequestSerializer, RouteResponseSerializer

class RouteCalculatorView(APIView):
    def post(self, request):
        serializer = RouteRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        start = data['start']
        end = data['end']
        vehicle_range = 400
        search_radius = 100
        mpg = 10

        try:
            
            route, distance = RoutingService.get_route(start, end)
            
           
            fuel_df = FuelService.load_fuel_data()
            
            
            segments = RoutingService.get_segment_points(route, vehicle_range)
            
            
            stops = FuelService.find_cheapest_stations(fuel_df, segments, search_radius)
            
            
            total_cost = RoutingService.compute_total_cost(distance, stops, mpg)


            
            
            response_data = {
                "total_distance": round(distance, 2),
                "total_cost": total_cost,
                "fuel_stops": stops,
              
             
            }
            
            response_serializer = RouteResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.validated_data)
            return Response(response_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)