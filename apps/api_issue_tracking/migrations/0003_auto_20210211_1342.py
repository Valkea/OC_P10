# Generated by Django 3.1.6 on 2021-02-11 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_issue_tracking", "0002_auto_20210211_1335"),
    ]

    operations = [
        migrations.RenameField(
            model_name="issue",
            old_name="members",
            new_name="contributors",
        ),
    ]
