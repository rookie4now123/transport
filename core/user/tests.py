import pytest
from .models import User

data_user = {
    "username": "test_user",
    "email": "test@gmail.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "123456",
    "user_type": "WEB"
}

@pytest.mark.django_db
def test_create_user():
    user = User.objects.acreate_user(**data_user)
    assert user.username == data_user["username"]
    assert user.email == data_user["email"]
    assert user.first_name == data_user["first_name"]
    assert user.last_name == data_user["last_name"]
    assert user.user_type == data_user["user_type"]