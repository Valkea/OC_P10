from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


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
        FEAT = "FEAT", "Feature"
        TASK = "TASK", "Task"

    class Priority(models.TextChoices):
        LOW = "L", "Low"
        MEDIUM = "M", "Medium"
        HIGH = "H", "High"

    class Status(models.TextChoices):
        TODOS = "TODO", "New"
        OPENED = "OPENED", "Opened"
        CLOSED = "CLOSED", "Closed"

    title = models.CharField("Title", max_length=128)

    description = models.TextField("Description", max_length=8192)

    tag = models.CharField("Tag", max_length=4, choices=Tag.choices, default=Tag.BUG)

    priority = models.CharField(
        "Priority", max_length=1, choices=Priority.choices, default=Priority.LOW
    )

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="project_issues",
    )

    status = models.CharField(
        "Status", max_length=6, choices=Status.choices, default=Status.TODOS
    )

    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name="author_user",
    )

    assignee_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name="assignee_user",
        blank=True,
        null=True,
    )

    created_time = models.DateTimeField("Creation date", auto_now_add=True)

    def __str__(self):
        return f"ISSUE: {self.title}"


class Comment(models.Model):

    description = models.TextField("Description", max_length=8192)

    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comment_author",
    )

    issue = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        related_name="comment_issue",
    )

    created_time = models.DateTimeField("Creation date", auto_now_add=True)

    def __str__(self):
        return f"COMMENT: {self.description[:20]}..."


class Contributor(models.Model):
    """This model is automatically created by the ManyToManyField in the Project,
    but as we need to add some extra fields, we must redefine it as a through model.
    """

    class Meta:
        unique_together = (("user", "project"),)

    class Role(models.TextChoices):
        ADMINISTRATOR = "ADMIN", "Administrator"
        CONTRIBUTOR = "CONTRIB", "Contributor"

    class Permission(models.TextChoices):
        NONE = "NONE", "No permission"
        READONLY = "READ", "Read Only"
        ALL = "ALL", "Read & Write"

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributor_user",
    )

    project = models.ForeignKey(
        to=Project,
        # on_delete=models.SET(get_sentinel_user),
        on_delete=models.CASCADE,
    )

    permission = models.CharField(
        "Permission", max_length=10, choices=Permission.choices, default=Permission.ALL
    )

    role = models.CharField(
        "Role", max_length=10, choices=Role.choices, default=Role.ADMINISTRATOR
    )

    def __str__(self):
        return f"CONTRIBUTOR: {self.user.username}"
