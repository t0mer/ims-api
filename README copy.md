# IMS Weather API

A FastAPI wrapper for the [py-weatheril](https://github.com/t0mer/py-weatheril) Python package, providing a RESTful API interface to Israel Meteorological Service (IMS) weather data.

## Features

- Get current weather analysis for any location in Israel
- Retrieve 5-day weather forecasts with hourly data
- Support for both Hebrew and English languages
- Complete location database (100+ cities, national parks, and tourist sites)

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd ims-api
```

2. Build and run with Docker Compose:
```bash
docker-compose up -d
```

The API will be available at `http://localhost:8000`

### Manual Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the service is running, visit:
- API Documentation: `http://localhost:8000/docs`
- ReDoc Documentation: `http://localhost:8000/redoc`

## API Endpoints

### GET /locations
Get all available locations with their IDs.

### GET /weather/current/{location_id}
Get current weather analysis for a specific location.

**Parameters:**
- `location_id` (int): Location ID (see locations endpoint for full list)
- `language` (str, optional): Language code ("he" or "en", default: "he")

### GET /weather/forecast/{location_id}
Get 5-day weather forecast with hourly data.

**Parameters:**
- `location_id` (int): Location ID
- `language` (str, optional): Language code ("he" or "en", default: "he")

### GET /health
Health check endpoint.

## Example Usage

### Get Current Weather for Tel Aviv
```bash
curl "http://localhost:8000/weather/current/2?language=en"
```

### Get Forecast for Jerusalem
```bash
curl "http://localhost:8000/weather/forecast/1?language=he"
```

## Popular Location IDs

- 1: ירושלים (Jerusalem)
- 2: תל-אביב, חוף (Tel Aviv, Coast)
- 3: חיפה (Haifa)
- 21: רעננה (Raanana)
- 31: אילת (Eilat)
- 8: באר שבע (Beer Sheva)
- 50: צפת (Safed)
- 267: מצדה (Masada)

For a complete list with Hebrew names, use the `/locations` endpoint.

## Environment Variables

No environment variables are required for basic operation.

## License

This project is licensed under the MIT License.

## Credits

This API wrapper is based on the excellent [py-weatheril](https://github.com/t0mer/py-weatheril) package by [t0mer](https://github.com/t0mer).