import re

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CpfBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None
        cpf_limpo = re.sub(r'[^0-9]', '', username)
        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=cpf_limpo)
        except user_model.DoesNotExist:
            return None
        if not user.has_usable_password():
            return user
        elif user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
