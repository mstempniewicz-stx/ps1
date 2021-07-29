import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from accounts.models import User
from base.views import ProtectedDataView

PROTECTED_DATA_API_URL = reverse("base:protected_data")


@pytest.mark.django_db
class TestBaseApiView:
    def test_protected_data_view(
        self, request_factory: APIRequestFactory, user: User
    ) -> None:

        request = request_factory.get(PROTECTED_DATA_API_URL)
        force_authenticate(request, user=user)

        response = ProtectedDataView.as_view()(request)
        assert response.status_code == HTTP_200_OK

    def test_protected_data_view_without_token(self, client: APIClient) -> None:
        response = client.get(PROTECTED_DATA_API_URL)
        assert response.status_code == HTTP_403_FORBIDDEN
