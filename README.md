# Transport Monitor API

Transport Monitor is a Django REST backend for managing school transport data and live route tracking. It supports two client roles:

- `WEB` users manage stations, routes, students, and review tracking data.
- `MONITOR` users log in from a mobile client, start route runs, upload GPS points, and end runs.

The project uses PostGIS for geospatial data, JWT for authentication, and Server-Sent Events for live location streaming.

## Stack

- Python 3.12
- Django 5
- Django REST Framework
- Simple JWT
- Channels + Daphne
- PostgreSQL + PostGIS
- GeoDjango / GDAL
- Pytest

## Project Layout

```text
transport/
+-- CoreRoot/               Django project settings and root URLs
+-- core/
|   +-- auth/               Auth serializers, permissions, and login/register viewsets
|   +-- user/               Custom user model and user endpoints
|   +-- abstract/           Shared base model/serializer/viewset helpers
|   +-- filters.py          Shared filters
|   +-- routers.py          Main API routing
+-- station/                Station model, serializer, viewset, tests
+-- route/                  Route and RouteSchedule domain logic
+-- student/                Student assignment APIs
+-- tracking/               Route runs, GPS points, SSE stream
+-- docker-compose.yml      Local PostGIS + app stack
+-- Dockerfile              Container image definition
+-- run_simulation.py       Single monitor tracking simulation script
+-- run_simulation_multi.py Multi-monitor tracking simulation script
+-- pytest.ini              Test configuration
```

## Domain Model

- `User` is a custom auth model with `WEB`, `MONITOR`, and `PARENT` types.
- `Station` stores a name, address, GIS point, and creator.
- `Route` represents a route definition.
- `RouteSchedule` links a route to a station plus day/time scheduling metadata.
- `Student` can be assigned to a specific `RouteSchedule`.
- `RouteRun` is one live or completed execution of a route by a monitor.
- `LocationPoint` stores GPS coordinates uploaded during a route run.

## API Surface

Base URL: `/api/`

### Auth

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `POST /api/monitor/auth/login/`

### Web user endpoints

- `GET|PATCH /api/user/`
- `GET|POST|PATCH|DELETE /api/monitors/`
- `GET|POST|PATCH|DELETE /api/station/`
- `GET|POST|PATCH|DELETE /api/route/`
- `GET|POST|PATCH|DELETE /api/student/`
- `GET /api/routeruns/`
- `GET /api/locationpoints/`
- `GET /api/location-stream/`

### Monitor endpoints

- `POST|PATCH /api/monitor/routeruns/`
- `POST /api/monitor/locationpoints/`

## Typical Flows

### 1. Web login

```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "web001",
  "password": "123456"
}
```

Successful login returns JWT tokens and serialized user data.

### 2. Monitor login

```http
POST /api/monitor/auth/login/
Content-Type: application/json

{
  "username": "monitor001",
  "password": "123456"
}
```

### 3. Start a route run

```http
POST /api/monitor/routeruns/
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "route": "<route-uuid>"
}
```

### 4. Upload a location point

```http
POST /api/monitor/locationpoints/
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "run": "<run-uuid>",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

### 5. End a route run

```http
PATCH /api/monitor/routeruns/<run-uuid>/
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "status": "COMPLETED"
}
```

### 6. Review location history from the web app

```http
GET /api/locationpoints/?route_name=Morning%20Express&date=2025-07-03
Authorization: Bearer <access-token>
```

The `tracking` app exposes filterable location history and an SSE stream at `/api/location-stream/` for live updates.

## Local Setup

### Prerequisites

- Python 3.12+
- PostgreSQL with PostGIS
- GDAL / GeoDjango system dependencies

If you run locally without Docker, make sure the GeoDjango native libraries are installed. The project currently uses the PostGIS backend in [CoreRoot/settings.py](/d:/reactProject/transport/CoreRoot/settings.py:92).

### Install and run

```bash
git clone <your-repo-url>
cd transport
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

For ASGI deployment, the codebase is set up for:

```bash
daphne CoreRoot.asgi:application
```

## Docker

The repo includes a ready-to-run Docker setup with PostGIS:

```bash
docker compose up --build
```

This starts:

- `db` using `postgis/postgis:15-3.4`
- `web` on port `8000`

The container startup runs migrations automatically through `entrypoint.sh`.

## Environment / Database Defaults

The following settings are read from environment variables, with defaults already defined in the project:

- `DB_NAME=transport`
- `DB_USER=postgres`
- `DB_PASSWORD=qwerty123456`
- `DB_HOST=db`
- `DB_PORT=5432`

## Testing

Pytest is configured through `pytest.ini`.

Run the test suite with:

```bash
pytest
```

Current tests cover:

- auth registration and login flows
- monitor tracking lifecycle
- station APIs
- route APIs
- student APIs

## Simulation Scripts

Two helper scripts exist for exercising the tracking flow:

- `run_simulation.py` logs in a monitor, starts a run, uploads location points, and completes the run.
- `run_simulation_multi.py` does the same in parallel for multiple configured monitors.

Before using them, update the hard-coded credentials, route UUIDs, and coordinates inside each script.

## CORS

The backend currently allows local frontend origins:

- `http://localhost:5173`
- `http://127.0.0.1:5173`

## Notes

- The app depends on PostGIS and geospatial libraries; plain PostgreSQL is not enough.
- The location stream uses an in-memory Channels layer by default, which is fine for local development but not for multi-instance production.
- An older README referenced external sample data. If that dataset is still needed, the existing historical link is: `https://drive.google.com/file/d/1vB1FeXLCC7dl6Onbp2SaJ0ZwEk2Ji166/view?usp=drive_link`
