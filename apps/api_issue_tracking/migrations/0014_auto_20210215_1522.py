# Generated by Django 3.1.6 on 2021-02-15 15:22

import apps.api_issue_tracking.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api_issue_tracking", "0013_auto_20210215_1521"),
    ]

    operations = [
        migrations.AlterField(
            model_name="issue",
            name="assignee_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET(apps.api_issue_tracking.models.get_sentinel_user),
                related_name="assignees",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
