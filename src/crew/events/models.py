from django.db import models
from django.utils import timezone

from users.models import User


class Event(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=128)
    text = models.TextField()

    participants_limit = models.PositiveSmallIntegerField(
            blank=True, 
            verbose_name='maximum number of participants',
            null=True,
        )
    price = models.PositiveIntegerField(
            blank=True, 
            verbose_name='price in rubles',
            null=True
        )
    link_to_chat = models.URLField(blank=True, null=True)
    event_date = models.DateTimeField()

    publication_date = models.DateField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def approve(self):
        self.is_approved = True
        self.publication_date = timezone.now()

    def __repr__(self):
        return f'Event({self.title}, pk={self.pk})'


