import csv
import io

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
import pytest

from apps.accounts.models import User
from apps.experiments.models import Dataset, Experiment


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


@pytest.fixture
def csv_file() -> SimpleUploadedFile:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["col1", "col2"])
    writer.writerow(["val1", "val2"])
    return SimpleUploadedFile(
        "test.csv",
        buffer.getvalue().encode("utf-8"),
        content_type="text/csv",
    )


@pytest.fixture
def dataset(user: User, csv_file: SimpleUploadedFile) -> Dataset:
    return Dataset.objects.create(
        name="Test dataset",
        version="1.0",
        file=csv_file,
        owner=user,
    )
