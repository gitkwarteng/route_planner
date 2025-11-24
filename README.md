# Route Planner API with Fuel Optimization

Django API that calculates optimal fuel stops along a route based on fuel prices.

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py load_stations
python manage.py runserver
```

## API Endpoint

**URL:** `http://localhost:8000/api/plan-route/`

**Methods:** GET or POST

**Parameters:**
- `start` - Starting location (e.g., "Los Angeles, CA")
- `finish` - Ending location (e.g., "Phoenix, AZ")

## Example Usage

### GET Request
```bash
curl "http://localhost:8000/api/plan-route/?start=Los%20Angeles,%20CA&end=Phoenix,%20AZ"
```

### POST Request
```bash
curl -X POST http://localhost:8000/api/plan-route/ \
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
  "total_gallons": 37.25
}
```

## Features

- Uses OpenRouteService for routing (1 API call per request)
- Optimizes fuel stops based on price and proximity to route
- Assumes 500-mile range and 10 MPG fuel efficiency
- Returns route geometry for map display
- Fast response times with database indexing
- Handles 8000+ fuel stations efficiently
- One-time geocoding via management command

## Loading Fuel Stations

1. Add stations to `fuel_stations.csv`:
```
OPIS Truckstop ID,Truckstop Name,Address,City,State,Rack ID,Retail Price
```

2. Run the management command:
```bash
python manage.py load_stations
```
