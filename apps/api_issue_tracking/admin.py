from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import Project, Issue, Comment, Contributor

# admin.site.register(Project)
# admin.site.register(Issue)
# admin.site.register(Comment)
# admin.site.register(Contributor)


class UserContribInline(admin.TabularInline):
    model = Contributor
    fk_name = "project"

    extra = 0

    verbose_name = "Contributor"
    verbose_name_plural = "Contributors"


class UserIssuesInline(admin.TabularInline):
    model = Issue
    fk_name = "project"

    extra = 0

    verbose_name = "Created Issue"
    verbose_name_plural = "Created Issues"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    inlines = [UserContribInline, UserIssuesInline]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "description",
                    "type",
                ]
            },
        ),
    ]

    list_display = (
        "title",
        "type",
    )

    list_filter = ("type", "contributors")


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "description",
                    "project",
                    "created_time",
                ]
            },
        ),
        (
            "Flags",
            {
                "fields": [
                    "tag",
                    "priority",
                    "status",
                ]
            },
        ),
        (
            "Users",
            {
                "fields": [
                    "author_user",
                    "assignee_user",
                ]
            },
        ),
    ]

    readonly_fields = ["created_time"]

    list_display = (
        "title",
        "tag",
        "priority",
        "status",
        "get_project",
    )

    list_filter = (
        "tag",
        "priority",
        "status",
        "project",
    )

    def get_project(self, obj):
        path = "admin:api_issue_tracking_project_change"
        url = reverse(path, args=(obj.project.id,))
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.project.title))

    get_project.admin_order_field = "project"  # Allows column order sorting
    get_project.short_description = "Associated Project"  # Renames column head


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "user",
                    "permission",
                    "role",
                    "project",
                ]
            },
        ),
    ]

    list_display = (
        "user",
        "permission",
        "role",
        "get_project",
    )

    list_filter = (
        "permission",
        "role",
        "project",
    )

    def get_project(self, obj):
        path = "admin:api_issue_tracking_project_change"
        url = reverse(path, args=(obj.project.id,))
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.project.title))

    get_project.admin_order_field = "project"  # Allows column order sorting
    get_project.short_description = "Associated Project"  # Renames column head


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "description",
                    "author_user",
                    "issue",
                    "created_time",
                ]
            },
        ),
    ]

    readonly_fields = ["author_user", "issue", "created_time", "description"]

    list_display = (
        "description",
        "author_user",
        "get_issue",
    )

    list_filter = (
        "author_user",
        "issue",
    )

    def get_issue(self, obj):
        path = "admin:api_issue_tracking_issue_change"
        url = reverse(path, args=(obj.issue.id,))
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.issue.title))

    get_issue.admin_order_field = "issue"  # Allows column order sorting
    get_issue.short_description = "Issue"  # Renames column head

    def has_add_permission(self, request, obj=None):
        return False
