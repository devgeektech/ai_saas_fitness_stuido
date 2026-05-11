from django.contrib import admin
from django.urls import path
from studio.views import classes, views


urlpatterns = [
    path("admin/dashboard", views.studio_admin_dashboard, name="studio-admin-dashboard"),
    path("admin/profile", views.studio_admin_profile, name="studio-admin-profile"),
    
    
    # classes
    path("classes", classes.index, name="classes-index"),
    path("classes/list", classes.ClassesListView.as_view(), name="classes-list"),
    path("classes/create", classes.create, name="classes-create"),
    path("classes/edit/<uuid:uuid>", classes.edit, name="classes-edit"),
    path("classes/view/<uuid:uuid>", classes.view, name="classes-view"),
    path("classes/delete/<uuid:uuid>", classes.delete, name="classes-delete"),
]
