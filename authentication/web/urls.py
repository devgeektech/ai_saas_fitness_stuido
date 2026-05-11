from django.contrib import admin
from django.urls import path
from authentication.web import views


urlpatterns = [
    
    path("admin/login", views.auth_login, name="admin-login"),
    path("profile", views.profile, name="profile"),
    path("admin/logout", views.auth_logout, name="admin-logout"),
    path("clear_logs", views.clear_logs, name="clear_logs"),
 
]