# Generated by Django 3.1.6 on 2021-02-13 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_issue_tracking', '0010_auto_20210211_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributor_user', to=settings.AUTH_USER_MODEL),
        ),
    ]