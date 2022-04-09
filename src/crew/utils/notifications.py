from django.core.mail import message
from users.models import User
from .email import send_crew_email


def _notify_staff(subject='', message=''):
    recipient = _get_staff_list()
    send_crew_email.delay(recipient, subject, message)


def _get_staff_list():
    return [user.email for user in User.objects.filter(is_staff=True)]


def notify_staff_to_publish(event):
    absolute_link_to_event = event.get_link_to_event()

    subject = 'Нужно проверить событие на crew.online'
    message = f'Проверь новое событие по ссылке: {absolute_link_to_event}'

    _notify_staff(subject, message)


def notify_user_publication_decision(event, comment=''):
    absolute_link_to_event = event.get_link_to_event()
    
    recipient = event.get_event_author().email

    if comment:
        subject = f'Событие {event.title} не прошло модерацию'
        message = f'''Ваше событие {event.title} не прошло модерацию.
            Комментарий: {comment}
            Отредактируйте событие: {absolute_link_to_event}'''
    else:
        subject = f'Событие {event.title} опубликовано'
        message = f'''Ваше событие {event.title} прошло модерацию.
            Доступно по ссылке {absolute_link_to_event}'''
        
    send_crew_email.delay([recipient], subject, message)


def notify_staff_approve_user(user):
    absolute_link_to_user = user.get_link_to_user()

    subject = 'Нужно проверить профиль новоприбывшего на crew.online'
    message = f'Проверь профиль чувака(ихи): {absolute_link_to_user}'

    _notify_staff(subject, message)


def notify_user_profile_approve_decision(user, comment=''):
    absolute_link_to_user = user.get_link_to_user()

    recipient = user.email

    if comment:
        subject = 'Ваш профиль на crew.online был отклонен:('
        message = f'''Нашим модераторам чем-то не понравился ваш профиль.
        Комментарий: {comment}
        Отредактируйте профиль: {absolute_link_to_user}'''
    else:
        subject = 'Ваш профиль прошел модерацию на crew.online'
        message = f'''Поздравляем! Теперь заходите и ищите новую компанию!
        Ваш профиль: {absolute_link_to_user}'''

    send_crew_email.delay([recipient], subject, message)
