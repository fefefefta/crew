from utils.email import send_crew_email
from utils.notifications import notify_staff


def notify_staff_to_publish(event):
    absolute_link_to_event = event.get_link_to_event()

    subject = 'Нужно проверить событие на crew.online'
    message = f'Проверь новое событие по ссылке: {absolute_link_to_event}'

    notify_staff(subject, message)


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
        
    send_crew_email([recipient], subject, message)
