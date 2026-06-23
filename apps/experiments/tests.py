from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse_lazy
from rest_framework.test import APIClient
import pytest

from apps.accounts.models import User
from apps.experiments.models import Dataset, Experiment


@pytest.mark.django_db
def test_list_experiments_requires_auth(api_client: APIClient) -> None:
    url = reverse_lazy("experiment-list")

    response = api_client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_create_experiment(auth_client: APIClient, user: User) -> None:
    url = reverse_lazy("experiment-list")

    response = auth_client.post(
        url,
        data={"title": "New experiment", "description": "A description"},
        format="json",
    )

    assert response.status_code == 201
    assert response.data["title"] == "New experiment"
    assert response.data["owner"] == user.pk


@pytest.mark.django_db
def test_create_experiment_requires_auth(api_client: APIClient) -> None:
    url = reverse_lazy("experiment-list")

    response = api_client.post(
        url,
        data={"title": "New experiment", "description": "A description"},
        format="json",
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_retrieve_experiment(auth_client: APIClient, experiment: Experiment) -> None:
    url = reverse_lazy("experiment-detail", kwargs={"pk": experiment.pk})

    response = auth_client.get(url)

    assert response.status_code == 200
    assert response.data["title"] == experiment.title


@pytest.mark.django_db
def test_update_experiment(auth_client: APIClient, experiment: Experiment) -> None:
    url = reverse_lazy("experiment-detail", kwargs={"pk": experiment.pk})

    response = auth_client.patch(
        url,
        data={"title": "Updated title", "description": "Updated description"},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["title"] == "Updated title"


@pytest.mark.django_db
def test_delete_experiment(auth_client: APIClient, experiment: Experiment) -> None:
    url = reverse_lazy("experiment-detail", kwargs={"pk": experiment.pk})

    response = auth_client.delete(url)

    assert response.status_code == 204
    assert Experiment.objects.count() == 0


@pytest.mark.django_db
def test_list_experiments(auth_client: APIClient, experiment: Experiment) -> None:
    url = reverse_lazy("experiment-list")

    response = auth_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == experiment.title


# ── Dataset tests ──────────────────────────────────────────────────────


@pytest.mark.django_db
def test_upload_csv(
    auth_client: APIClient, csv_file: SimpleUploadedFile, user: User
) -> None:
    url = reverse_lazy("dataset-upload")

    response = auth_client.post(
        url,
        {"name": "New dataset", "version": "1.0", "file": csv_file},
        format="multipart",
    )

    assert response.status_code == 201
    assert response.data["name"] == "New dataset"
    assert response.data["owner"] == user.pk


@pytest.mark.django_db
def test_upload_csv_requires_auth(
    api_client: APIClient, csv_file: SimpleUploadedFile
) -> None:
    url = reverse_lazy("dataset-upload")

    response = api_client.post(
        url,
        {"name": "New dataset", "version": "1.0", "file": csv_file},
        format="multipart",
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_upload_csv_invalid_extension(auth_client: APIClient) -> None:
    url = reverse_lazy("dataset-upload")
    file = SimpleUploadedFile(
        "data.txt", b"not a csv content", content_type="text/plain"
    )

    response = auth_client.post(
        url, {"name": "Bad dataset", "version": "1.0", "file": file}, format="multipart"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_list_datasets(auth_client: APIClient, dataset: Dataset) -> None:
    url = reverse_lazy("dataset-list")

    response = auth_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == dataset.name


@pytest.mark.django_db
def test_retrieve_dataset(auth_client: APIClient, dataset: Dataset) -> None:
    url = reverse_lazy("dataset-detail", kwargs={"pk": dataset.pk})

    response = auth_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == dataset.name


@pytest.mark.django_db
def test_retrieve_dataset_not_owner(
    api_client: APIClient, user_data: dict[str, str], dataset: Dataset
) -> None:
    other_user = User.objects.create_user(
        email="other@test.com", password="test123", username="other"
    )
    api_client.force_authenticate(user=other_user)
    url = reverse_lazy("dataset-detail", kwargs={"pk": dataset.pk})

    response = api_client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_dataset(auth_client: APIClient, dataset: Dataset) -> None:
    url = reverse_lazy("dataset-detail", kwargs={"pk": dataset.pk})

    response = auth_client.delete(url)

    assert response.status_code == 204
    assert Dataset.objects.count() == 0


@pytest.mark.django_db
def test_download_dataset(auth_client: APIClient, dataset: Dataset) -> None:
    url = reverse_lazy("dataset-download", kwargs={"pk": dataset.pk})

    response = auth_client.get(url)

    assert response.status_code == 200
    assert response["Content-Type"] == "text/csv"
    assert "attachment" in response["Content-Disposition"]


@pytest.mark.django_db
def test_download_dataset_requires_auth(
    api_client: APIClient, dataset: Dataset
) -> None:
    url = reverse_lazy("dataset-download", kwargs={"pk": dataset.pk})

    response = api_client.get(url)

    assert response.status_code == 401
