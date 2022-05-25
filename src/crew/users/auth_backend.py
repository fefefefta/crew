from django.contrib.auth.backends import ModelBackend

from .models import User, LoginCode


class PasswordlessAuthBackend(ModelBackend):
    def authenticate(self, request, email='', code='', **kwargs):
        user = User.objects.get(email=email)
        if (LoginCode.check_code(user, code) and
                self.user_can_authenticate(user)):
            return user
