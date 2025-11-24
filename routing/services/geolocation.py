import enum

from routing.data import Coordinate


class LocationServiceType(enum.IntEnum):
    OPEN_STREET_MAPS = 0
    GOOGLE_MAPS = 1

    @property
    def is_open_street_maps(self):
        return self == LocationServiceType.OPEN_STREET_MAPS

    @property
    def is_google_maps(self):
        return self == LocationServiceType.GOOGLE_MAPS


class GeoLocationService:
    service_class = None

    def __init__(self, service_type:LocationServiceType = LocationServiceType.OPEN_STREET_MAPS):
        self.service_type = service_type
        self.service_class = self.get_service_class()
        if not self.service_class:
            raise ValueError(f"Invalid service type: {service_type}")

        self.geocoder = self.service_class(user_agent="route_planner")

    def get_service_class(self):
        if self.service_type.is_open_street_maps:
            from geopy.geocoders import Nominatim
            return Nominatim
        elif self.service_type.is_google_maps:
            from geopy.geocoders import GoogleV3
            return GoogleV3
        else:
            raise ValueError(f"Invalid service type: {self.service_type}")

    def geocode(self, location:str) -> Coordinate:
        result = self.geocoder.geocode(location)
        return Coordinate(latitude=result.latitude, longitude=result.longitude) if result else None