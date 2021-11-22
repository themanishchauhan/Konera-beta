# Generated by Django 3.2.8 on 2021-11-19 08:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('auth_token', models.CharField(max_length=100)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=64)),
                ('ano', models.IntegerField(null=True)),
                ('date_of_exam', models.DateField(blank=True, null=True)),
                ('profile_pic', models.FileField(default='', upload_to='accounts/profile_picture')),
                ('your_address', models.CharField(blank=True, max_length=150, null=True)),
                ('exam_centre', models.CharField(blank=True, max_length=150, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
