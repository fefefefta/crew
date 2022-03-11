from django.contrib.auth.models import AbstractUser
from django.db import models


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
        return f"User(username={self.username}, full_name={self.full_name})"

    def __str__(self):
        return self.username
