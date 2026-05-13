from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from authentication.web import views as auth_view


urlpatterns = [
    path("dj-admin/", admin.site.urls),
    path("", auth_view.auth_login),
    path("", include("authentication.web.urls")),
    path("admin/", include("superadmin.urls")),
    path("studio/", include("studio.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)