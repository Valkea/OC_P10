# Generated by Django 3.1.6 on 2021-02-11 14:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_issue_tracking', '0003_auto_20210211_1342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='contributors',
        ),
        migrations.AddField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(related_name='contributors', to=settings.AUTH_USER_MODEL),
        ),
    ]
