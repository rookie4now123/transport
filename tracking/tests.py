import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.gis.geos import Point
from route.models import Route
from tracking.models import RouteRun, LocationPoint
from core.user.models import User, UserType

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def monitor_user(db):
    return User.objects.acreate_user(
        username="monitor_user",
        email="monitor@example.com",
        password="password123",
        user_type=UserType.MONITOR
    )

@pytest.fixture
def web_user(db):
    return User.objects.acreate_user(
        username="web_user",
        email="web@example.com",
        password="password123",
        user_type=UserType.WEB
    )

@pytest.fixture
def route(db):
    return Route.objects.create(route_name="Tracking Route")

@pytest.mark.django_db
class TestTrackingAPI:
    mobile_run_endpoint = '/api/monitor/routeruns/'
    mobile_location_endpoint = '/api/monitor/locationpoints/'
    web_run_endpoint = '/api/routeruns/'
    web_location_endpoint = '/api/locationpoints/'

    def test_start_route_run(self, api_client, monitor_user, route):
        api_client.force_authenticate(user=monitor_user)
        data = {"route": str(route.id)}
        response = api_client.post(self.mobile_run_endpoint, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == 'IN_PROGRESS'
        assert RouteRun.objects.filter(monitor=monitor_user, route=route).exists()

    def test_upload_location_point(self, api_client, monitor_user, route):
        api_client.force_authenticate(user=monitor_user)
        run = RouteRun.objects.create(route=route, monitor=monitor_user)
        data = {
            "run": str(run.id),
            "latitude": 40.7128,
            "longitude": -74.0060
        }
        response = api_client.post(self.mobile_location_endpoint, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert LocationPoint.objects.filter(run=run).exists()

    def test_web_view_runs(self, api_client, web_user, monitor_user, route):
        api_client.force_authenticate(user=web_user)
        RouteRun.objects.create(route=route, monitor=monitor_user)
        response = api_client.get(self.web_run_endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_end_route_run(self, api_client, monitor_user, route):
        api_client.force_authenticate(user=monitor_user)
        run = RouteRun.objects.create(route=route, monitor=monitor_user, status='IN_PROGRESS')
        data = {"status": "COMPLETED"}
        response = api_client.patch(f"{self.mobile_run_endpoint}{run.id}/", data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'COMPLETED'
        run.refresh_from_db()
        assert run.status == 'COMPLETED'
        assert run.end_time is not None
