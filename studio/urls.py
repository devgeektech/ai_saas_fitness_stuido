from django.contrib import admin
from django.urls import path
from studio import views


urlpatterns = [
    path("admin/dashboard", views.studio_admin_dashboard, name="studio-admin-dashboard")
]
