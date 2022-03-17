from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey

from crew.settings import AUTH_USER_MODEL


class User(AbstractUser):
    """
    User class.
    """
    username = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=False) 

    def __repr__(self):
        return "User(username={}, full_name={}, email={})".format(
                    self.username, self.full_name, self.email,
                )

    def __str__(self):
        return self.username


class EmailConfirmationCode(models.Model):
    """
    Class defines user-code, 
    """

    # TIME_TO_LIVE = 

    user = models.OneToOneField(AUTH_USER_MODEL, 
                                on_delete=models.CASCADE)
    code = models.CharField(max_length=32, unique=True)

    def is_active(self):
        pass

    def __repr__(self):
        return "EmailConfirmationCode(username={})".format(
                    self.user.username,
                )
