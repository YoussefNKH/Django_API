# DjangoAPI

this project is a Django REST API for calculating optimal fuel stops and costs along a route in the United States. It uses real fuel price data and routing logic to help drivers find the cheapest places to refuel on their journey.

## Features

- Calculate routes between two points in the US.
- Suggest optimal fuel stops based on vehicle range and fuel prices.
- Compute total trip distance and estimated fuel cost.
- RESTful API endpoints.

## Project Structure

- `spotterapi/` - Django project settings and configuration.
- `routes/` - Main app containing API views, serializers, services, and URLs.
- `static/data/fuel-prices-for-be-assessment-clean.csv` - Fuel price dataset.

## Requirements

- Python 3.8+
- Django 3.2+
- Django REST Framework

Install dependencies:

```sh
pip install -r requirements.txt
```
## Environment Variables

Before running the project, create a `.env` file in the BASE directory with the following content:

```
TOMTOM_API_KEY=your_tomtom_api_key_here
```

You must obtain a [TomTom API key](https://developer.tomtom.com/) and set it as `TOMTOM_API_KEY` in the `.env` file.
## Usage

### Running the Server Locally

```sh
python manage.py runserver
```

### Running with Docker

Build and run the Docker container:

```sh
docker build -t spotterapi .
docker run -p 8000:8000 spotterapi
```

The API will be available at `http://localhost:8000/`.

### API Endpoint

- **POST** `/api/routes/`

#### Request Body

```json
{
  "start": [latitude, longitude],
  "end": [latitude, longitude]
}
```

#### Example

```json
{
  "start": [34.0522, -118.2437],
  "end": [36.1699, -115.1398]
}
```

#### Response

```json
{
  "total_distance": 430.5,
  "total_cost": 120.75,
  "fuel_stops": [
    {
      "name": "TA SAGINAW I 75 TRAVEL CENTER",
      "location": [43.323835, -83.874172],
      "price": 3.299
    }
  ]
}
```

## Development

- Main API logic in [`RouteCalculatorView`](routes/views.py)
- Routing and fuel logic in [`fuel_service.py`](routes/services/fuel_service.py) and `routing_service.py`
- Serializers in [`serializers.py`](routes/serializers.py)
- URL configuration in [`urls.py`](spotterapi/urls.py) and [`routes/urls.py`](routes/urls.py)
