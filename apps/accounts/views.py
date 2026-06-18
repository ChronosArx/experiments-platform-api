from typing import cast

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from apps.accounts.models import User
from apps.accounts.serializers import (
    ChangePasswordSerializer,
    UserRegistrationSerializer,
    UserRestrationResponseSerializer,
)
from apps.accounts.services import UserServices


@extend_schema(
    tags=["Auth"],
    auth=[],
    responses={201: UserRestrationResponseSerializer},
)
class UserRegistrationView(generics.CreateAPIView[User]):
    serializer_class = UserRegistrationSerializer

    def create(self, request: Request, *args: object, **kwargs: object) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        response_serializer = UserRestrationResponseSerializer(
            {
                "email": user.email,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Auth"])
class UserLoginView(TokenObtainPairView):
    pass


@extend_schema(
    tags=["Auth"],
    request=ChangePasswordSerializer,
    responses={204: None},
)
class UserChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args: object, **kwargs: object) -> Response:
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        UserServices.change_password(
            user=cast(User, request.user),
            old_password=serializer.validated_data["old_password"],
            new_password=serializer.validated_data["new_password"],
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
