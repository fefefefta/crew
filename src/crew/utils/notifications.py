from users.models import User
from .email import send_crew_email


# def notify_about_new_user(user):
#     pass


def notify_staff(subject='', message=''):
    recipient = _get_staff_list()
    send_crew_email.delay(recipient, subject, message)


def _get_staff_list():
    return [user.email for user in User.objects.filter(is_staff=True)]
