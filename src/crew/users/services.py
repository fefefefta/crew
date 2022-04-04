from uuid import uuid4

from django.shortcuts import get_object_or_404

from .models import EmailConfirmationCode, User
from utils.email import send_crew_email


def initiate_email_confirmation(user):
    """
    It makes a secret code for user and creates an object of 
    EmailConfirmationCode. Then it makes a link of following pattern:
        https://<domain_name>/reg/confirmation/<secret_code> 
    and send it to user email.    

    After requesting this link user.is_active attribute will be changed on True
    and EmailConfirmationCode object will be removed from db. The process of 
    confirming will be finished.

    """

    secret_code = EmailConfirmationCode.create_for_user(user)
    _send_secret_link_to_user(user, secret_code)


def _create_secret_code_for_user(user):

    # TODO: добавить обработку по времени действия кода

    secret_code = str(uuid4()).replace('-', '')

    EmailConfirmationCode.objects.update_or_create(
            user=user,
            defaults={'code': secret_code})

    return secret_code


def _send_secret_link_to_user(user, secret_code):
    secret_link = f"http://127.0.0.1:8000/reg/confirmation/{secret_code}"

    subject = "Подтверждение регистрации на crew.online"
    message = f"Перейдите по ссылке и аккаунт будет активирован: {secret_link}"

    send_crew_email.delay([user.email], subject, message)


def finish_email_confirmation(confirmation_code):
    """
    It identify user by secret confirmation code, turn its is_active attribute
    to True and delete user-code object from db. If user is not able to be 
    identified, raises 404.

    """
    user = EmailConfirmationCode.check_code(code=confirmation_code)

    user.activate()
    user.save()

    # TODO notification about user registration


def get_user_by_email(email: str):
    try:
        user = User.objects.get(email=email)

    except User.DoesNotExist:
        raise Exception('no user with that nickname')

    return user


def send_login_code_to_user(user, code):
    subject = 'Код подтверждения для входа'
    message = f'Ваш код: {code}'

    send_crew_email.delay([user.email], subject, message)
