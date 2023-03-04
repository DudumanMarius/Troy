from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
    path("lessons/", include(
        ("transcript.urls", "transcript"), namespace="lessons")),
    path("users/", include(("users.urls", "users"), namespace="users")),
    path("classes/", include(("classes.urls", "classes"), namespace="classes"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
