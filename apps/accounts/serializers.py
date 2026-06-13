from typing import Any

from rest_framework import serializers

from apps.accounts.models import User


class ChangePasswordSerializer(serializers.Serializer[dict[str, Any]]):
    old_password = serializers.CharField(
        required=True,
        style={"input_type": "password"},
    )
    new_password = serializers.CharField(
        required=True,
        style={"input_type": "password"},
    )
    new_password2 = serializers.CharField(
        required=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError(
                {"new_password2": "Las contraseñas no coinciden"}
            )
        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer[User]):
    password2 = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password2"]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
            },
        }

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password2": "Las contraseñas no coinciden"}
            )
        return attrs

    def create(self, validated_data: dict[str, Any]) -> User:
        validated_data.pop("password2")
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class UserRestrationResponseSerializer(serializers.Serializer[dict[str, Any]]):
    email = serializers.EmailField()
    access = serializers.CharField()
    refresh = serializers.CharField()
