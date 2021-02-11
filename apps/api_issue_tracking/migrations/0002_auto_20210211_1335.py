# Generated by Django 3.1.6 on 2021-02-11 13:35

import apps.api_issue_tracking.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_issue_tracking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='assignee_user',
            field=models.ForeignKey(on_delete=models.SET(apps.api_issue_tracking.models.get_sentinel_user), related_name='assignees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issue',
            name='author_user',
            field=models.ForeignKey(on_delete=models.SET(apps.api_issue_tracking.models.get_sentinel_user), related_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issue',
            name='members',
            field=models.ManyToManyField(related_name='contributors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_issues', to='api_issue_tracking.project'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author_user',
            field=models.ForeignKey(on_delete=models.SET(apps.api_issue_tracking.models.get_sentinel_user), related_name='comment_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_issue', to='api_issue_tracking.issue'),
        ),
    ]
