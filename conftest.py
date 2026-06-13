from rest_framework.test import APIClient
import pytest


@pytest.fixture
def api_client() -> APIClient:
    api_client = APIClient()
    return api_client


@pytest.fixture
def user_data() -> dict[str, str]:
    return {
        "username": "test",
        "email": "test@test.com",
        "password": "test123",
        "password2": "test123",
    }
