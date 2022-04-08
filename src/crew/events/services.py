from utils.notifications import notify_staff


def notify_staff_to_publish(event):
    absolute_link_to_event = event.get_link_to_event()

    subject = 'Нужно проверить событие на crew.online'
    message = f'Проверь новое событие по ссылке: {absolute_link_to_event}'

    notify_staff(subject, message)
