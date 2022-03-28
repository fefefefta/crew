from datetime import timedelta
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from crew.settings import AUTH_USER_MODEL
from utils.stuff import random_number


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

    def activate(self):
        self.is_active = True

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

    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=32, unique=True)

    @classmethod
    def create_for_user(cls, user):
        secret_code = str(uuid4()).replace('-', '')

        cls.objects.update_or_create(
            user=user,
            defaults={'code': secret_code})

        return secret_code

    def __repr__(self):
        return "EmailConfirmationCode(username={})".format(
                    self.user.username,
                )


class LoginCode(models.Model):
    ATTEMPTS_LIMIT = 3
    CODE_REQUESTING_LIMIT = 5

    TIME_TO_LIVE = timedelta(minutes=15)
    CODE_LENGTH = 6

    code = models.CharField(max_length=32)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True)

    attempts = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    @classmethod
    def create_for_user(cls, user: User):
        last_codes_count = cls._get_last_codes(user).count()

        if last_codes_count >= cls.CODE_REQUESTING_LIMIT:
            raise Exception('too many codes requested. wait some time.')

        return cls.objects.create(
                code=random_number(cls.CODE_LENGTH),
                user=user,
                created_at=timezone.now(),
                expires_at=timezone.now() + cls.TIME_TO_LIVE,
            )

    @classmethod
    def check_code(cls, user: User, code: str):
        last_code = cls._get_last_codes(user).first()

        if not last_code:
            raise Exception('no codes found')

        if last_code.attempts > cls.ATTEMPTS_LIMIT:
            raise Exception('too many attempts. ask for new code.')

        if code != last_code.code:
            last_code.attempts += 1
            last_code.save()            
            raise Exception('Invalid code') 

        cls.objects.filter(user=user).delete()
        return last_code.user

    @classmethod
    def _get_last_codes(cls, user: User):
        return cls.objects.filter(
                user=user, 
                created_at__gte=timezone.now() - cls.TIME_TO_LIVE
            ).order_by("-created_at")
        
    def __repr__(self):
        return "LoginCode(username={})".format(self.user.username)
