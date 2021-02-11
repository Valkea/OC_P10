from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# from apps.users.models import User  # TODO define AUTH_USER_MODEL in settings.py


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="deleted")[0]


class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACKEND = 0, "Back-end"
        FRONTEND = 1, "Front-end"
        IOS = 2, "iOS"
        ANDROID = 3, "Android"

    title = models.CharField("Title", max_length=128)

    description = models.TextField("Description", max_length=8192)

    type = models.PositiveSmallIntegerField(
        "Type", choices=ProjectType.choices, default=ProjectType.BACKEND
    )

    # author_user = models.ForeignKey(
    #         to=settings.AUTH_USER_MODEL,
    #         on_delete=models.SET(get_sentinel_user),
    #         )

    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="contributors", through='Contributor'
    )


class Issue(models.Model):
    class Tag(models.TextChoices):
        BUG = 0, "Bug"
        FEAT = 1, "Amélioration"
        TASK = 2, "Tâche"

    class Priority(models.TextChoices):
        LOW = 0, "Faible"
        MEDIUM = 1, "Moyenne"
        HIGH = 2, "Élevée"

    class Status(models.TextChoices):
        TODOS = 0, "À faire"
        OPENED = 1, "En cours"
        CLOSED = 2, "Terminé"

    title = models.CharField("Title", max_length=128)

    description = models.TextField("Description", max_length=8192)

    tag = models.PositiveSmallIntegerField(
        "Balise", choices=Tag.choices, default=Tag.BUG
    )

    priority = models.PositiveSmallIntegerField(
        "Priorité", choices=Priority.choices, default=Priority.LOW
    )

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="project_issues",
    )

    status = models.PositiveSmallIntegerField(
        "Statut", choices=Status.choices, default=Status.TODOS
    )

    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name="author",
    )

    assignee_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name="assignees",
    )

    created_time = models.DateTimeField("Date de création", auto_now_add=True)


class Comment(models.Model):

    description = models.TextField("Description", max_length=8192)

    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name="comment_author",
    )

    issue = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        related_name="comment_issue",
    )

    created_time = models.DateTimeField("Date de création", auto_now_add=True)


class Contributor(models.Model):  # TODO pas sur du tout !
    """ This model is automatically created by the ManyToManyField in the Project,
    but as we need to add some extra fields, we must redefine it as a through model.
    """

    class Role(models.TextChoices):
        OWNER = 0, "Responsable"
        CONTRIBUTOR = 1, "Contributeur"

    class Permission(models.TextChoices):
        NONE = 0, "Aucune permission"
        READONLY = 1, "Lecture uniquement"
        ALL = 3, "Lecture & Ecriture"

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # TODO
    )

    project = models.ForeignKey(
        to=Project,
        on_delete=models.SET(get_sentinel_user),
    )

    permission = models.PositiveSmallIntegerField(
        "Permission", choices=Permission.choices, default=Permission.ALL
    )

    role = models.PositiveSmallIntegerField(
        "Rôle", choices=Role.choices, default=Role.OWNER
    )
