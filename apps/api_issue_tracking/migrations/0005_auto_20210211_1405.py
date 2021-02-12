# Generated by Django 3.1.6 on 2021-02-11 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_issue_tracking', '0004_auto_20210211_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.PositiveSmallIntegerField(choices=[('0', 'Aucune permission'), ('1', 'Lecture uniquement'), ('3', 'Lecture & Ecriture')], default='3', max_length=1, verbose_name='Permission')),
                ('role', models.PositiveSmallIntegerField(choices=[('0', 'Responsable'), ('1', 'Contributeur')], default='0', max_length=1, verbose_name='Rôle')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_contributors', to='api_issue_tracking.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributor_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='contributors',
        ),
        migrations.AddField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(related_name='contributors', through='api_issue_tracking.Contributor', to=settings.AUTH_USER_MODEL),
        ),
    ]