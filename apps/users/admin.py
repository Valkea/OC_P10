from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .models import User
from apps.api_issue_tracking.models import Contributor, Issue, Comment

# admin.site.register(User)
admin.site.unregister(Group)


class UserContribInline(admin.TabularInline):
    """
    Inline for displaying the various roles taken in
    the projects by a given user directly on it's admin page.
    """

    model = Contributor
    fk_name = "user"

    extra = 0

    verbose_name = "Collaboration"
    verbose_name_plural = "Collaborations"

    readonly_fields = ["user", "project", "permission", "role"]

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


class UserIssuesInline(admin.TabularInline):
    """
    Inline for displaying the created Issues
    of a given user directly on it's admin page.
    """

    model = Issue
    fk_name = "author_user"

    extra = 0

    verbose_name = "Created Issue"
    verbose_name_plural = "Created Issues"

    readonly_fields = [
        "title",
        "description",
        "tag",
        "priority",
        "project",
        "status",
        "author_user",
        "assignee_user",
    ]

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


class UserAssigneesInline(admin.TabularInline):
    """
    Inline for displaying the assigned Issues
    of a given user directly on it's admin page.
    """

    model = Issue
    fk_name = "assignee_user"

    extra = 0

    verbose_name = "Assigned Issue"
    verbose_name_plural = "Assigned Issues"

    readonly_fields = [
        "title",
        "description",
        "tag",
        "priority",
        "project",
        "status",
        "author_user",
        "assignee_user",
    ]

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


class UserCommentsInline(admin.TabularInline):
    """
    Inline for displaying the Comments of a given user
    directly on it's admin page.
    """

    model = Comment
    fk_name = "author_user"

    extra = 0

    verbose_name = "Wrote Comment"
    verbose_name_plural = "Wrote Comments"

    readonly_fields = [
        "description",
        "issue",
    ]

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


@admin.register(User)
class UserAdmin(UserAdmin):
    """ Define the 'Users' admin section behaviors & displays. """

    inlines = [
        UserContribInline,
        UserIssuesInline,
        UserAssigneesInline,
        UserCommentsInline,
    ]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "username",
                    "password",
                    "first_name",
                    "last_name",
                    "email",
                ]
            },
        ),
        (
            "Status",
            {
                "classes": [
                    "collapse",
                ],
                "fields": ["is_active", "is_staff", "is_superuser"],
            },
        ),
        (
            "Dates",
            {
                "fields": ["date_joined", "last_login"],
            },
        ),
    ]
    readonly_fields = ["date_joined", "last_login"]

    list_display = (
        "username",
        "email",
    )
    list_filter = ("is_active",)
