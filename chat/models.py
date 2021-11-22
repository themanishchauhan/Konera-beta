from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
from datetime import datetime
from accounts.models import Profile

User = get_user_model()

# Create your models here.
class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        profile = kwargs.get('profile')
        lookup = Q(first_person=profile) | Q(second_person=profile)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
        
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    sender=models.CharField(max_length=120)
    message=models.CharField(max_length=1000000)
    date=models.DateTimeField(default=datetime.now,blank=True)
    def __str__(self):
        return self.message
