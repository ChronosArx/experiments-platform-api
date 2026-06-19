from rest_framework.test import APIClient
import pytest

from apps.accounts.models import User
from apps.experiments.models import Experiment


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


@pytest.fixture
def user(user_data: dict[str, str]) -> User:
    return User.objects.create_user(
        email=user_data["email"],
        password=user_data["password"],
        username=user_data["username"],
    )


@pytest.fixture
def auth_client(api_client: APIClient, user: User) -> APIClient:
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def experiment(user: User) -> Experiment:
    return Experiment.objects.create(
        title="Test experiment",
        description="Test description",
        owner=user,
    )
