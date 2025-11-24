# Route Planner API with Fuel Optimization

Django API that calculates optimal fuel stops along a route based on fuel prices.

## Setup

### Docker (Recommended)

```bash
# Start services
make up

# Load fuel stop points with geocoded data from fixtures
make load-data

# View logs
make logs

# Stop services
make down
```

### Manual Setup

```bash
pip install -r requirements/base.txt
python manage.py migrate
python manage.py load_stations fuel_stations.csv
python manage.py runserver
```

**Requirements:**
- PostgreSQL with PostGIS extension
- Redis server
- Python 3.11+

## API Endpoint

**URL:** `http://localhost:8000/api/route/plan/`

**Methods:** GET or POST

**Parameters:**
- `start` - Starting location (e.g., "Los Angeles, CA")
- `finish` - Ending location (e.g., "Phoenix, AZ")

## Example Usage

### GET Request
```bash
curl "http://localhost:8000/api/route/?start=Los%20Angeles,%20CA&end=Phoenix,%20AZ"
```

### POST Request
```bash
curl -X POST http://localhost:8000/api/route/ \
  -H "Content-Type: application/json" \
  -d '{"start": "Los Angeles, CA", "end": "Phoenix, AZ"}'
```

## Response Format

```json
{
  "route": [[lon, lat], ...],
  "total_distance": 372.5,
  "stops": [
    {
      "name": "PILOT TRAVEL CENTER #1243",
      "location": "Gila Bend, AZ, USA",
      "price": 3.90,
      "gallons": 35.2,
      "cost": 137.28,
      "distance_from_start": 320.5
    }
  ],
  "total_fuel_cost": 145.23,
  "total_gallons": 37.25,
  "map": "https://www.openstreetmap.org/?mlat=36.7425836&mlon=-101.26182965#map=6/37.86/-102.66",
  "message": "successful"
}
```

## Features

- Uses OpenRouteService for routing (1 API call per request)
- Optimizes fuel stops based on price and proximity to route
- Assumes 500-mile range and 10 MPG fuel efficiency
- Returns route geometry for map display
- Fast response times with database indexing
- Handles 8000+ fuel stations efficiently
- One-time geocoding via management command and fixtures

## Loading Fuel Stations

1. Add stations to `fuel_stations.csv`:
```
OPIS Truckstop ID,Truckstop Name,Address,City,State,Rack ID,Retail Price
```

2. Run the management command:
```bash
# Docker
make load-data

# Manual
python manage.py loaddata fuel_stations
```

## Docker Commands

```bash
make up           # Start all services
make down         # Stop all services
make restart      # Restart services
make logs         # View logs
make shell        # Access container shell
make migrate      # Run migrations
make load-data    # Load fixture data
make dump-data    # Dump data to fixture
```
