import json
from http.client import CREATED

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from accounts.models import User
from accounts.views import UserRegisterView

REGISTER_API_URL = reverse("accounts:register")
MY_ACCOUNT_API_URL = reverse("accounts:me")
ACCOUNT_EMAIL_STATUS_API_URL = reverse("accounts:status")


@pytest.mark.django_db(transaction=False)
class TestUsersApiView:
    def test_user_register_view(
        self, request_factory: APIRequestFactory, user_data: dict
    ) -> None:
        data = {
            "email": user_data.get("email"),
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "password": user_data.get("password"),
        }

        request = request_factory.post(
            REGISTER_API_URL, json.dumps(data), content_type="application/json"
        )

        response = UserRegisterView.as_view()(request)
        assert response.status_code == CREATED

    def test_user_register_view_without_email(
        self, request_factory: APIRequestFactory, user_data: dict
    ) -> None:
        data = {
            "email": "nomail",
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "password": user_data.get("password"),
        }

        request = request_factory.post(
            REGISTER_API_URL, json.dumps(data), content_type="application/json"
        )

        response = UserRegisterView.as_view()(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_confirm_email_view(self, client: APIClient, user: User) -> None:
        response = client.get(
            reverse(
                "accounts:confirm_email", kwargs={"activation_key": user.activation_key}
            )
        )

        assert response.status_code == status.HTTP_200_OK

    def test_user_confirm_email_view_only_once(
        self, client: APIClient, user: User
    ) -> None:
        response = client.get(
            reverse(
                "accounts:confirm_email", kwargs={"activation_key": user.activation_key}
            )
        )

        assert response.status_code == status.HTTP_200_OK

        response = client.get(
            reverse(
                "accounts:confirm_email", kwargs={"activation_key": user.activation_key}
            )
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_email_confirmation_status_view(
        self, client: APIClient, authorization_header: dict
    ) -> None:
        response = client.get(ACCOUNT_EMAIL_STATUS_API_URL, **authorization_header)

        assert response.status_code == status.HTTP_200_OK

    def test_user_email_confirmation_status_view_unauthorized(
        self, client: APIClient
    ) -> None:
        response = client.get(ACCOUNT_EMAIL_STATUS_API_URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
