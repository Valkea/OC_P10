"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf.urls import url

from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

import debug_toolbar

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("rest_framework.urls")),  # login / logout
    path("", include("apps.api_issue_tracking.urls")),
    path("", include("apps.users.urls")),
    path("auth-jwt/", obtain_jwt_token, name="login-jwt"),
    path("auth-jwt-refresh/", refresh_jwt_token, name="renew-jwt"),
    path("auth-jwt-verify/", verify_jwt_token, "verify-jwt"),
    url("", RedirectView.as_view(pattern_name="login-jwt", permanent=False)),
    path("__debug__/", include(debug_toolbar.urls)),
]
