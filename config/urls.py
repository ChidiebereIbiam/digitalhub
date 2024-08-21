from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("digitalhub.core.urls")),
    path("blog/", include("digitalhub.blog.urls")),
    path("profile/", include("digitalhub.userbase.urls")),
    path("authentication/", include("allauth.urls")),
    path("authentication/", include("digitalhub.authentication.urls")),
]
