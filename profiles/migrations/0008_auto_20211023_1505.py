# Generated by Django 3.2.7 on 2021-10-23 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0007_remove_reward_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reward',
            name='user_profile',
        ),
        migrations.AddField(
            model_name='reward',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
