from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from accounts.models import Profile
User = get_user_model()
# Create your models here.

class Feedback(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,blank=True,null=True)
    text = models.CharField(max_length=1024, blank=True,null=True)
    date=models.DateTimeField(default=datetime.now,blank=True)
    def __str__(self):
        return self.user.user.username

