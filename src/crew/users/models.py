from datetime import timedelta
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import get_object_or_404, reverse
from django.utils import timezone

from crew.settings import AUTH_USER_MODEL, CREW_DOMAIN, STATUS_ON_MODERATION, \
    STATUS_APPROVED, STATUS_DECLINED
from utils.stuff import random_number


class User(AbstractUser):
    """My passwordless User-model"""

    username = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False) 
    moderation_status = models.CharField(
        max_length=32,
        default=STATUS_ON_MODERATION,
    )

    def activate(self):
        self.is_active = True
    
    def deactivate(self):
        self.is_active = False
    
    def get_link_to_user(self):
        """Return absolute link to user"""
        relative_link_to_user = reverse('profile', args=[self.username])
        absolite_link_to_user = f"{CREW_DOMAIN}{relative_link_to_user}"

        return absolite_link_to_user

    def is_approved(self):
        return True if self.moderation_status == STATUS_APPROVED else False

    def is_declined(self):
        return True if self.moderation_status == STATUS_DECLINED else False

    def is_on_moderation(self):
        return (True if self.moderation_status == STATUS_ON_MODERATION 
                    else False)
 
    @classmethod
    def get_user_by_email(cls, email: str):
        try:
            user = cls.objects.get(email=email)
        except cls.DoesNotExist:
            raise Exception('no user with that email')

        return user

    @classmethod
    def get_user_by_username(cls, username: str):
        try:
            user = cls.objects.get(username=username)
        except cls.DoesNotExist:
            raise Exception('no user with that username')

        return user    
    
    def approve(self):
        self.moderation_status = STATUS_APPROVED
        self.save()

    def decline(self):
        self.moderation_status = STATUS_DECLINED
        self.save()

    def __repr__(self):
        return "User(username={}, full_name={}, email={})".format(
                    self.username, self.full_name, self.email,
                )

    def __str__(self):
        return self.username


class EmailConfirmationCode(models.Model):
    """Class defines an email confirmation code""" 

    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=32, unique=True)

    @classmethod
    def create_for_user(cls, user):
        """It creates secret_code by uuid4 for taken User instance, then create 
        EmailConfirmationCode object or update existing for user and returns
        secret_code"""

        secret_code = str(uuid4()).replace('-', '')

        cls.objects.update_or_create(
            user=user,
            defaults={'code': secret_code})

        return secret_code

    @classmethod
    def check_code(cls, code):
        """
        It takes confirmation code, returns a user from EmailConfirmationCode 
        instance if it exists and delete that instance
        """

        user = get_object_or_404(EmailConfirmationCode, code=code).user
        EmailConfirmationCode.objects.get(code=code).delete()

        return user

    def __repr__(self):
        return "EmailConfirmationCode(username={})".format(
                    self.user.username,
                )


class LoginCode(models.Model):
    """
    Class defines a code being mailed to user to log in
    
    Attributes
        code: n-digit random code. n is a CODE_LENGTH constant
        user: an instance of the User model for which a login code is created
        created_at: datetime of creating
        expires_at: created_at + TIME_TO_LIVE constant
        attempts: code entry attempt counter, not code request counter    

    """

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
        """Compare last created code for user with taken code. If equal then it
        delete all LoginCodes for user and return that user. If not or if 
        some conditions not met then raise exceptions"""
        
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
        """Takes User instance and returns recently created LoginCode 
           instances for user"""

        return cls.objects.filter(
                user=user, 
                created_at__gte=timezone.now() - cls.TIME_TO_LIVE
            ).order_by("-created_at")
        
    def __repr__(self):
        return "LoginCode(username={})".format(self.user.username)
