from django.urls import reverse_lazy
from rest_framework.test import APIClient
import pytest

from apps.accounts.models import User
from apps.experiments.models import Experiment


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
