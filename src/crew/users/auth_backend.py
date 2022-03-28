from django.contrib.auth.backends import ModelBackend

from .models import User, LoginCode


class PasswordlessAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, code=None, **kwargs):
        user = User._default_manager.get_by_natural_key(username)
        if (LoginCode.check_code(user, code) and 
                self.user_can_authenticate(user)):
            return user
