# Generated by Django 3.1.6 on 2021-02-11 14:07

import apps.api_issue_tracking.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api_issue_tracking", "0005_auto_20210211_1405"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contributor",
            name="permission",
            field=models.PositiveSmallIntegerField(
                choices=[
                    ("0", "Aucune permission"),
                    ("1", "Lecture uniquement"),
                    ("3", "Lecture & Ecriture"),
                ],
                default="3",
                verbose_name="Permission",
            ),
        ),
        migrations.AlterField(
            model_name="contributor",
            name="project",
            field=models.ForeignKey(
                on_delete=models.SET(apps.api_issue_tracking.models.get_sentinel_user),
                to="api_issue_tracking.project",
            ),
        ),
        migrations.AlterField(
            model_name="contributor",
            name="role",
            field=models.PositiveSmallIntegerField(
                choices=[("0", "Responsable"), ("1", "Contributeur")],
                default="0",
                verbose_name="Rôle",
            ),
        ),
        migrations.AlterField(
            model_name="contributor",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
