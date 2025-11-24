import logging
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .client import RoutingClient
from .serializers import RouteRequestSerializer
from routing.services.route import RouteService
from .services.geolocation import GeoLocationService
from .services.station import StationService
from routing.utils.route import make_response

logger = logging.getLogger(__name__)


class RouteViewSet(ViewSet):
    serializer_class = RouteRequestSerializer

    def list(self, request):
        return Response({
            'message': 'Route Planning API',
            'endpoints': {
                'plan': '/api/route/plan/ - Plan a route with fuel stops (GET/POST)'
            }
        })

    @action(detail=False, methods=['get', 'post'])
    def plan(self, request):
        logger.info(f"{request.method} request from {request.META.get('REMOTE_ADDR')}")
        data = request.query_params if request.method == 'GET' else request.data
        serializer = self.serializer_class(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            start = serializer.validated_data['start']
            finish = serializer.validated_data['finish']
            logger.info(f"Planning route: {start} to {finish}")

            geolocation = GeoLocationService()

            client = RoutingClient()

            start_location = geolocation.geocode(start)
            finish_location = geolocation.geocode(finish)

            # Get route data
            route = client.get_route(
                from_location=start_location,
                to_location=finish_location
            )
            if not route:
                return Response({'error': 'No route found'}, status=status.HTTP_404_NOT_FOUND)

            # Get sample stop points
            route_points = StationService.get_sample_points_along_route(
                with_coordinates=route.coordinates
            )

            route_service = RouteService()
            result = route_service.get_optimized_stops_for_route(
                with_points=route_points,
                total_distance=route.distance
            )
            logger.info(f"Route planned successfully: {route.distance} miles")
            return Response(make_response(
                route=route,
                fuel_stops=result.stops,
                total_cost=result.cost,
                total_gallons=result.gallons,
                message="Successful"
            ))
        except ValidationError as e:
            logger.warning(f"Validation error: {e.detail}")
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error planning route: {str(e)}", exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
