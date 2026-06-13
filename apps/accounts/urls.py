from django.urls import path

from apps.accounts.views import (
    UserChangePasswordView,
    UserLoginView,
    UserRegistrationView,
)


urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path(
        "change-password/",
        UserChangePasswordView.as_view(),
        name="user-change-password",
    ),
]
