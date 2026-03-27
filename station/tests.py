import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.gis.geos import Point
from station.models import Station
from core.user.models import User, UserType

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.acreate_user(
        username="test_user",
        email="test@example.com",
        password="testpassword123",
        user_type=UserType.WEB,
        first_name="Test",
        last_name="User"
    )

@pytest.fixture
def station_data():
    return {
        "station_name": "Central Station",
        "address": "123 Main St",
        "location": {"latitude": 40.7128, "longitude": -74.0060}
    }

@pytest.mark.django_db
class TestStationAPI:
    endpoint = '/api/station/'

    def test_get_stations_unauthenticated(self, api_client):
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_stations_authenticated(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK

    def test_create_station(self, api_client, user, station_data):
        api_client.force_authenticate(user=user)
        response = api_client.post(self.endpoint, station_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['station_name'] == station_data['station_name']
        assert response.data['location']['latitude'] == station_data['location']['latitude']
        assert response.data['location']['longitude'] == station_data['location']['longitude']
        assert response.data['creator'] == user.username

    def test_create_station_invalid_location(self, api_client, user):
        api_client.force_authenticate(user=user)
        invalid_data = {
            "station_name": "Invalid Station",
            "address": "456 Error St",
            "location": {"latitude": "not-a-float", "longitude": -74.0060}
        }
        response = api_client.post(self.endpoint, invalid_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_station(self, api_client, user):
        api_client.force_authenticate(user=user)
        # Create a station first
        station = Station.objects.create(
            station_name="Old Name",
            address="Old Address",
            location=Point(-74.0060, 40.7128),
            creator=user
        )
        
        update_data = {"station_name": "New Name"}
        response = api_client.patch(f"{self.endpoint}{station.id}/", update_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['station_name'] == "New Name"

    def test_delete_station(self, api_client, user):
        api_client.force_authenticate(user=user)
        station = Station.objects.create(
            station_name="Delete Me",
            address="Some Address",
            location=Point(-74.0060, 40.7128),
            creator=user
        )
        response = api_client.delete(f"{self.endpoint}{station.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Station.objects.filter(id=station.id).count() == 0
