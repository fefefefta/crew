from django.db import models
from django.urls import reverse
from django.utils import timezone

from crew.settings import CREW_DOMAIN, STATUS_ON_MODERATION, STATUS_APPROVED, \
    STATUS_DECLINED
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
    moderation_status = models.CharField(
        max_length=32, 
        default=STATUS_ON_MODERATION,
    )

    def get_link_to_event(self):
        """Return absolute link to event"""
        relative_link_to_event = reverse('event', args=[self.pk])
        absolite_link_to_event = f"{CREW_DOMAIN}{relative_link_to_event}"

        return absolite_link_to_event

    def get_event_author(self):
        return self.author

    def is_approved(self):
        return True if self.moderation_status == STATUS_APPROVED else False

    def is_on_moderation(self):
        return (True if self.moderation_status == STATUS_ON_MODERATION
                    else False)

    def is_declined(self):
        return True if self.moderation_status == STATUS_DECLINED else False
    
    @classmethod
    def get_by_pk(cls, pk):
        return cls.objects.get(pk=pk)

    def approve(self):
        self.moderation_status = STATUS_APPROVED
        self.publication_date = timezone.now()
        self.save()

    def decline(self):
        self.moderation_status = STATUS_DECLINED
        self.save()

    def __repr__(self):
        return f'Event(pk={self.pk}, {self.title[:20]}, {self.author.username})'


