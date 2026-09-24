from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            usuario = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            return None

        if usuario.check_password(password):
            return usuario

        return None
    