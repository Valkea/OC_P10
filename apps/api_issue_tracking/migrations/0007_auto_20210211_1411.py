# Generated by Django 3.1.6 on 2021-02-11 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_issue_tracking', '0006_auto_20210211_1407'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='contributors',
            new_name='contributors_through',
        ),
    ]
