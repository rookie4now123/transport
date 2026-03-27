import pytest
from rest_framework import status
from rest_framework.test import APIClient
from core.user.models import User, UserType

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestAuthAPI:
    register_endpoint = '/api/auth/register/'
    login_endpoint = '/api/auth/login/'
    monitor_login_endpoint = '/api/monitor/auth/login/'

    def test_register_web_user(self, api_client):
        data = {
            "username": "new_web_user",
            "email": "new_web@example.com",
            "first_name": "New",
            "last_name": "Web",
            "password": "password123"
        }
        response = api_client.post(self.register_endpoint, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert "access" in response.data or "token" in response.data
        assert User.objects.filter(username="new_web_user", user_type=UserType.WEB).exists()

    def test_login_web_user(self, api_client):
        # Create a web user first
        user = User.objects.acreate_user(
            username="test_web",
            password="password123",
            user_type=UserType.WEB
        )
        data = {
            "username": "test_web",
            "password": "password123"
        }
        response = api_client.post(self.login_endpoint, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert response.data['user']['username'] == "test_web"

    def test_login_web_user_invalid_type(self, api_client):
        # Create a monitor user but try to login through web endpoint
        user = User.objects.acreate_user(
            username="test_monitor",
            password="password123",
            user_type=UserType.MONITOR
        )
        data = {
            "username": "test_monitor",
            "password": "password123"
        }
        response = api_client.post(self.login_endpoint, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_monitor_user(self, api_client):
        user = User.objects.acreate_user(
            username="test_monitor",
            password="password123",
            user_type=UserType.MONITOR
        )
        data = {
            "username": "test_monitor",
            "password": "password123"
        }
        response = api_client.post(self.monitor_login_endpoint, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert response.data['user']['username'] == "test_monitor"
