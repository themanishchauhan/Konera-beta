from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=64)
    ano = models.IntegerField(null=True)
    date_of_exam = models.DateField(null=True, blank=True)
    profile_pic = models.FileField(upload_to='accounts/profile_picture', default="")
    your_address = models.CharField(max_length=150,null=True,blank=True)
    exam_centre = models.CharField(max_length=150,null=True,blank=True)

    def __str__(self):
        return self.user.username


