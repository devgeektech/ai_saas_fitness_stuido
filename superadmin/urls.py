from django.urls import path
from superadmin.views import auth

urlpatterns = [
    path("dashboard/", auth.admin_dashboard, name="admin-dashboard"),
    path("studios/", auth.studios, name="studios-index"),
    path("studios/list/", auth.StudioUsersListView.as_view(), name="studios-list"),
    path("studios/toggle-status/<uuid:uuid>/", auth.toggle_studio_user_status, name="studios-toggle-status"),
    path("studios/view/<uuid:uuid>/", auth.view_studio, name="studios-view"),
]
