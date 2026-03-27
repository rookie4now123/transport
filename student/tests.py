import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.gis.geos import Point
from station.models import Station
from route.models import Route, RouteSchedule
from student.models import Student
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
def station(db):
    return Station.objects.create(
        station_name="Student Station",
        address="Student Address",
        location=Point(0, 0)
    )

@pytest.fixture
def route(db):
    return Route.objects.create(route_name="Student Route")

@pytest.fixture
def schedule(db, route, station):
    return RouteSchedule.objects.create(
        route=route,
        station=station,
        day_of_week="MON",
        time_of_day="AM",
        arrival_time="08:00:00"
    )

@pytest.mark.django_db
class TestStudentAPI:
    endpoint = '/api/student/'

    def test_create_student(self, api_client, web_user, schedule):
        api_client.force_authenticate(user=web_user)
        data = {
            "student_id": "S123",
            "first_name": "John",
            "last_name": "Doe",
            "grade": "10",
            "class_name": "A",
            "is_bus_rider": True,
            "assignment_id": str(schedule.id)
        }
        response = api_client.post(self.endpoint, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['first_name'] == "John"
        assert response.data['assignment_details']['id'] == str(schedule.id)

    def test_get_students(self, api_client, web_user):
        api_client.force_authenticate(user=web_user)
        Student.objects.create(student_id="S456", first_name="Jane", last_name="Smith")
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_update_student_assignment(self, api_client, web_user, schedule):
        api_client.force_authenticate(user=web_user)
        student = Student.objects.create(student_id="S789", first_name="Bob", last_name="Brown")
        
        data = {"assignment_id": str(schedule.id)}
        response = api_client.patch(f"{self.endpoint}{student.id}/", data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['assignment_details']['id'] == str(schedule.id)

    def test_delete_student(self, api_client, web_user):
        api_client.force_authenticate(user=web_user)
        student = Student.objects.create(student_id="S000", first_name="To", last_name="Delete")
        response = api_client.delete(f"{self.endpoint}{student.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Student.objects.filter(id=student.id).count() == 0
