import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.gis.geos import Point
from station.models import Station
from route.models import Route, RouteSchedule
from core.user.models import User, UserType

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def web_user(db):
    return User.objects.acreate_user(
        username="web_user",
        email="web@example.com",
        password="password123",
        user_type=UserType.WEB
    )

@pytest.fixture
def monitor_user(db):
    return User.objects.acreate_user(
        username="monitor_user",
        email="monitor@example.com",
        password="password123",
        user_type=UserType.MONITOR
    )

@pytest.fixture
def station(db):
    return Station.objects.create(
        station_name="Test Station",
        address="Test Address",
        location=Point(0, 0)
    )

@pytest.mark.django_db
class TestRouteAPI:
    endpoint = '/api/route/'

    def test_create_route(self, api_client, web_user, station, monitor_user):
        api_client.force_authenticate(user=web_user)
        data = {
            "route_name": "Route 1",
            "monitors_ids": [str(monitor_user.id)],
            "schedule_data": [
                {
                    "station": str(station.id),
                    "day_of_week": "MON",
                    "time_of_day": "AM",
                    "arrival_time": "08:00:00"
                }
            ]
        }
        response = api_client.post(self.endpoint, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['route_name'] == "Route 1"
        assert len(response.data['schedule_entries']) == 1
        assert response.data['schedule_entries'][0]['station']['id'] == str(station.id).replace('-', '')
        # Wait, the serializer uses format='hex' for UUIDs in AbstractSerializer
        # Let's check the response data id format.
        
    def test_get_routes(self, api_client, web_user):
        api_client.force_authenticate(user=web_user)
        Route.objects.create(route_name="Route A")
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_update_route_schedule(self, api_client, web_user, station):
        api_client.force_authenticate(user=web_user)
        route = Route.objects.create(route_name="Route B")
        RouteSchedule.objects.create(
            route=route,
            station=station,
            day_of_week="MON",
            time_of_day="AM",
            arrival_time="09:00:00"
        )
        
        # Update schedule
        data = {
            "route_name": "Updated Route B",
            "schedule_data": [
                {
                    "station": str(station.id),
                    "day_of_week": "TUE",
                    "time_of_day": "PM",
                    "arrival_time": "17:00:00"
                }
            ]
        }
        response = api_client.patch(f"{self.endpoint}{route.id}/", data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['route_name'] == "Updated Route B"
        assert len(response.data['schedule_entries']) == 1
        assert response.data['schedule_entries'][0]['day_of_week'] == "TUE"

    def test_delete_route(self, api_client, web_user):
        api_client.force_authenticate(user=web_user)
        route = Route.objects.create(route_name="To Delete")
        response = api_client.delete(f"{self.endpoint}{route.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Route.objects.filter(id=route.id).count() == 0
