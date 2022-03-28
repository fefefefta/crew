from django.core.mail import send_mail
from django.conf import settings

from crew.celery import app


@app.task
def send_crew_email(recipient, subject, message):
    send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient, 
            fail_silently=False,
        )
