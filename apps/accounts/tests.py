from django.urls import reverse_lazy
from rest_framework.test import APIClient
import pytest

from apps.accounts.models import User
from apps.accounts.services import UserServices


@pytest.mark.django_db
def test_register_success(api_client: APIClient, user_data: dict[str, str]) -> None:
    url = reverse_lazy("user-register")

    response = api_client.post(url, data=user_data, format="json")

    assert response.status_code == 201
    assert response.data["access"]
    assert response.data["refresh"]
    assert response.data["email"]


@pytest.mark.django_db
def test_register_passwrod_not_match(
    api_client: APIClient, user_data: dict[str, str]
) -> None:
    url = reverse_lazy("user-register")
    user_data["password2"] = "not_match"

    response = api_client.post(url, data=user_data, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_register_user_created(
    api_client: APIClient, user_data: dict[str, str]
) -> None:
    url = reverse_lazy("user-register")

    response = api_client.post(url, data=user_data, format="json")

    assert response.status_code == 201
    assert User.objects.count() == 1
    user = User.objects.first()
    assert user
    assert user.email == user_data["email"]


@pytest.mark.django_db
def test_register_duplicate_email(
    api_client: APIClient, user_data: dict[str, str]
) -> None:
    url = reverse_lazy("user-register")
    api_client.post(url, data=user_data, format="json")

    response = api_client.post(url, data=user_data, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_register_missing_email(
    api_client: APIClient, user_data: dict[str, str]
) -> None:
    url = reverse_lazy("user-register")
    user_data.pop("email")

    response = api_client.post(url, data=user_data, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_register_missing_password(
    api_client: APIClient, user_data: dict[str, str]
) -> None:
    url = reverse_lazy("user-register")
    user_data.pop("password")

    response = api_client.post(url, data=user_data, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_register_invalid_email(
    api_client: APIClient, user_data: dict[str, str]
) -> None:
    url = reverse_lazy("user-register")
    user_data["email"] = "invalid-email"

    response = api_client.post(url, data=user_data, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_success(api_client: APIClient, user_data: dict[str, str]) -> None:
    User.objects.create_user(
        email=user_data["email"],
        password=user_data["password"],
        username=user_data["username"],
    )
    url = reverse_lazy("user-login")
    user_data.pop("password2")
    user_data.pop("username")

    response = api_client.post(url, data=user_data, format="json")

    assert response.status_code == 200
    assert response.data["access"]
    assert response.data["refresh"]


@pytest.mark.django_db
def test_login_invalid_password(
    api_client: APIClient, user_data: dict[str, str]
) -> None:
    User.objects.create_user(
        email=user_data["email"],
        password=user_data["password"],
        username=user_data["username"],
    )
    url = reverse_lazy("user-login")

    response = api_client.post(
        url,
        data={"email": user_data["email"], "password": "wrong_password"},
        format="json",
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_login_user_not_found(api_client: APIClient) -> None:
    url = reverse_lazy("user-login")

    response = api_client.post(
        url,
        data={"email": "nonexistent@test.com", "password": "test123"},
        format="json",
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_login_missing_email(api_client: APIClient, user_data: dict[str, str]) -> None:
    url = reverse_lazy("user-login")

    response = api_client.post(
        url,
        data={"password": user_data["password"]},
        format="json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_missing_password(
    api_client: APIClient, user_data: dict[str, str]
) -> None:
    url = reverse_lazy("user-login")

    response = api_client.post(
        url,
        data={"email": user_data["email"]},
        format="json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_inactive_user(api_client: APIClient, user_data: dict[str, str]) -> None:
    User.objects.create_user(
        email=user_data["email"],
        password=user_data["password"],
        username=user_data["username"],
        is_active=False,
    )
    url = reverse_lazy("user-login")

    response = api_client.post(
        url,
        data={"email": user_data["email"], "password": user_data["password"]},
        format="json",
    )

    assert response.status_code == 401


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


@pytest.mark.django_db
def test_change_password_success(
    auth_client: APIClient, user_data: dict[str, str]
) -> None:
    url = reverse_lazy("user-change-password")

    response = auth_client.post(
        url,
        data={
            "old_password": user_data["password"],
            "new_password": "newpass123",
            "new_password2": "newpass123",
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.data["detail"] == "Contraseña actualizada correctamente"


@pytest.mark.django_db
def test_change_password_wrong_old_password(
    auth_client: APIClient,
) -> None:
    url = reverse_lazy("user-change-password")

    response = auth_client.post(
        url,
        data={
            "old_password": "wrong_password",
            "new_password": "newpass123",
            "new_password2": "newpass123",
        },
        format="json",
    )

    assert response.status_code == 400
    assert response.data["old_password"] == "La contraseña actual no es correcta"


@pytest.mark.django_db
def test_change_password_not_match(
    auth_client: APIClient,
) -> None:
    url = reverse_lazy("user-change-password")

    response = auth_client.post(
        url,
        data={
            "old_password": "test123",
            "new_password": "newpass123",
            "new_password2": "different",
        },
        format="json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_change_password_unauthenticated(api_client: APIClient) -> None:
    url = reverse_lazy("user-change-password")

    response = api_client.post(
        url,
        data={
            "old_password": "test123",
            "new_password": "newpass123",
            "new_password2": "newpass123",
        },
        format="json",
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_change_password_missing_fields(auth_client: APIClient) -> None:
    url = reverse_lazy("user-change-password")

    response = auth_client.post(url, data={}, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_user_services_change_password_raise_error_on_wrong_old_password(
    user: User,
) -> None:
    with pytest.raises(ValueError, match="La contraseña actual no es correcta"):
        UserServices.change_password(
            user=user,
            old_password="wrong",
            new_password="newpass123",
        )
