from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# from apps.users.models import User  # TODO define AUTH_USER_MODEL in settings.py


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="deleted")[0]


class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACKEND = "BE", "Back-end"
        FRONTEND = "FE", "Front-end"
        IOS = "IO", "iOS"
        ANDROID = "AN", "Android"

    title = models.CharField("Title", max_length=128)

    description = models.TextField("Description", max_length=8192)

    type = models.CharField(
        "Type", max_length=2, choices=ProjectType.choices, default=ProjectType.BACKEND
    )

    # author_user = models.ForeignKey(
    #         to=settings.AUTH_USER_MODEL,
    #         on_delete=models.SET(get_sentinel_user),
    #         )

    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="contributors", through="Contributor"
    )

    def __str__(self):
        return f"PROJECT: {self.title}"


class Issue(models.Model):
    class Tag(models.TextChoices):
        BUG = "BUG", "Bug"
        FEAT = "FEAT", "Amélioration"
        TASK = "TASK", "Tâche"

    class Priority(models.TextChoices):
        LOW = "L", "Faible"
        MEDIUM = "M", "Moyenne"
        HIGH = "H", "Élevée"

    class Status(models.TextChoices):
        TODOS = "TODO", "À faire"
        OPENED = "OPENED", "En cours"
        CLOSED = "CLOSED", "Terminé"

    title = models.CharField("Title", max_length=128)

    description = models.TextField("Description", max_length=8192)

    tag = models.CharField("Balise", max_length=4, choices=Tag.choices, default=Tag.BUG)

    priority = models.CharField(
        "Priorité", max_length=1, choices=Priority.choices, default=Priority.LOW
    )

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="project_issues",
    )

    status = models.CharField(
        "Statut", max_length=6, choices=Status.choices, default=Status.TODOS
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

    def __str__(self):
        return f"ISSUE: {self.title}"


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

    def __str__(self):
        return f"COMMENT: {self.description[:20]}..."


class Contributor(models.Model):  # TODO pas sur du tout !
    """This model is automatically created by the ManyToManyField in the Project,
    but as we need to add some extra fields, we must redefine it as a through model.
    """

    class Role(models.TextChoices):
        OWNER = "OWNER", "Responsable"
        CONTRIBUTOR = "CONTRIB", "Contributeur"

    class Permission(models.TextChoices):
        NONE = "NONE", "Aucune permission"
        READONLY = "READ", "Lecture uniquement"
        ALL = "ALL", "Lecture & Ecriture"

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # TODO
    )

    project = models.ForeignKey(
        to=Project,
        on_delete=models.SET(get_sentinel_user),
    )

    permission = models.CharField(
        "Permission", max_length=10, choices=Permission.choices, default=Permission.ALL
    )

    role = models.CharField(
        "Rôle", max_length=10, choices=Role.choices, default=Role.OWNER
    )

    def __str__(self):
        return f"CONTRIBUTOR: {self.user.username}"
