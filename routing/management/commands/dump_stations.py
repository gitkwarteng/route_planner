from pathlib import Path
from django.core.management.base import BaseCommand
from django.core import serializers
from routing.models import FuelStation


class Command(BaseCommand):
    help = 'Dump fuel stations to fixture file'
    
    def handle(self, *args, **options):
        fixtures_dir = Path(__file__).resolve().parent.parent.parent / 'fixtures'
        fixtures_dir.mkdir(exist_ok=True)
        
        fixture_path = fixtures_dir / 'fuel_stations.json'
        
        stations = FuelStation.objects.all()
        
        with open(fixture_path, 'w') as f:
            serializers.serialize('json', stations, indent=2, stream=f)
        
        self.stdout.write(self.style.SUCCESS(f'Dumped {stations.count()} stations to {fixture_path}'))
