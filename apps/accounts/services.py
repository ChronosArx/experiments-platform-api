from rest_framework.exceptions import ValidationError

from apps.accounts.models import User


class UserServices:
    @staticmethod
    def change_password(user: User, old_password: str, new_password: str) -> None:
        if not user.check_password(old_password):
            raise ValidationError(
                {"old_password": "La contraseña actual es incorrecta."}
            )
        user.set_password(new_password)
        user.save()
