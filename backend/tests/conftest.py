from typing import Dict

import django
import pytest
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User  # isort:skip

django.setup()


@pytest.fixture
def authorization_header(user: User) -> Dict:
    """
    Generate a token for user and return a dictionary with authorization header
    that can be used in client requests.
    """

    token = AccessToken.for_user(user)
    return {"HTTP_AUTHORIZATION": f"Bearer {str(token)}"}


@pytest.fixture
def client() -> APIClient:
    """
    Create a new APIClient, so we are sure that sessions and cookies are not shared
    between tests.
    """
    return APIClient()


@pytest.fixture()
def request_factory() -> APIRequestFactory:
    return APIRequestFactory()


@pytest.fixture(scope="module")
def user_data():
    return {
        "last_name": "Doe",
        "first_name": "John",
        "email": "John.Doe@example.com",
        "password": "passJohn1",
        "auth": "Sm9obi5Eb2VAZXhhbXBsZS5jb206cGFzc0pvaG4x",
    }


@pytest.fixture()
def superuser(user_data):
    superuser, _ = User.objects.get_or_create(
        email=user_data["email"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        is_staff=True,
        is_active=True,
        is_superuser=True,
    )
    return superuser


@pytest.fixture()
def user(user_data):
    user, _ = User.objects.get_or_create(
        password=user_data.get("password"),
        last_name=user_data.get("last_name"),
        first_name=user_data.get("first_name"),
        email=user_data.get("email"),
        is_staff=False,
        is_active=True,
        is_superuser=False,
    )
    return user
