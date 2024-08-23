from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("digitalhub.core.urls")),
    path("", include("digitalhub.payment.urls")),
    path("blog/", include("digitalhub.blog.urls")),
    path("profile/", include("digitalhub.userbase.urls")),
    path("authentication/", include("allauth.urls")),
    path("authentication/", include("digitalhub.authentication.urls")),
    path('authentication/', include('allauth.socialaccount.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
