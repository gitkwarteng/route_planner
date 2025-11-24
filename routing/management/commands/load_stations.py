import csv
import time
from pathlib import Path
from django.core.management.base import BaseCommand
from geopy.geocoders import Nominatim
from routing.models import FuelStation

class Command(BaseCommand):
    help = 'Load fuel stations from CSV and geocode them'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'file',
            type=str,
            nargs='?',
            default='data/fuel-stations.csv',
            help='Path to CSV file with fuel station data'
        )
    
    def handle(self, *args, **options):
        csv_path = Path(options['file'])
        if not csv_path.is_absolute():
            csv_path = Path(__file__).resolve().parent.parent.parent.parent / csv_path
        
        if not csv_path.exists():
            self.stdout.write(self.style.ERROR(f'File not found: {csv_path}'))
            return
        
        geocoder = Nominatim(user_agent="route_planner")

        FuelStation.objects.all().delete()
        stations = []

        processed = 0

        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                processed += 1
                try:
                    city = row['City'].strip()
                    state = row['State']
                    location = f"{city}, {state}, USA"
                    self.stdout.write(
                            f'{processed}. Processing station: {row["Truckstop Name"]} ({location})'
                    )
                    result = geocoder.geocode(location)

                    if result:
                        from django.contrib.gis.geos import Point
                        name = row['Truckstop Name'].strip()
                        address = row['Address']
                        stations.append(FuelStation(
                            opis_id=row['OPIS Truckstop ID'],
                            name=name,
                            address=address,
                            city=city,
                            state=state,
                            rack_id=row['Rack ID'],
                            price=float(row['Retail Price']),
                            location=Point(result.longitude, result.latitude)
                        ))
                    else:
                        self.stdout.write(self.style.WARNING(f"Failed to geocode: {location}"))

                    if len(stations) >= 100:
                        FuelStation.objects.bulk_create(stations)
                        self.stdout.write(f'Loaded {FuelStation.objects.count()} stations...')
                        stations = []

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error parsing: {location}. {e}"))
                    time.sleep(1)

        if stations:
            FuelStation.objects.bulk_create(stations)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {FuelStation.objects.count()} fuel stations'))
